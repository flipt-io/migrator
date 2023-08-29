import requests
from models.flipt import Documents, Document, Flag, FlagType, Variant, Segment, SegmentMatchType, Constraint, ConstraintComparisonType

class Transformer:
    BASE_URL = 'https://app.launchdarkly.com/api/v2'

    def __init__(self, api_key):
        self.api_key = api_key

    def transform(self) -> Documents:
        headers = {'Authorization': self.api_key}

        response = requests.get(f"{self.BASE_URL}/flags/default", headers=headers)
        if response.status_code != 200:
            raise Exception(f"Request to LaunchDarkly API failed with status code: {response.status_code}")

        data = response.json()
        documents = Documents(namespaces={})

        # environments is a map of env names to segments
        environments: dict[str, list[Segment]] = {}
        for f in data['items']:
            response = requests.get(f"{self.BASE_URL}/flags/default/{f['key']}", headers=headers)
            if response.status_code != 200:
                raise Exception(f"Request to LaunchDarkly API failed with status code: {response.status_code}")
            
            flag_data = response.json()

            # We do not support percentage based rollouts on segmentation for "boolean"
            # but LaunchDarkly does. So we will use the VARIANT_FLAG_TYPE for all flags.
            flag = Flag(
                key=flag_data['key'],
                name=flag_data['name'],
                description=flag_data['description'],
                enabled=False,
                type=FlagType.variant,
                variants=[],
            )

            for v in flag_data['variations']:
                variant = Variant(
                    key=str(v['value']),
                    name=str(v['value']), # LaunchDarkly does not support names for variants
                    description=v['description'] if 'description' in v else '',
                )
                flag.variants.append(variant)

            environment_data = flag_data["environments"]
            for environment in environment_data:
                if environment not in environments:
                    environments[environment] = []

                    response = requests.get(f"{self.BASE_URL}/segments/default/{environment}", headers=headers)

                    if response.status_code != 200:
                        raise Exception(f"Request to LaunchDarkly API failed with status code: {response.status_code}")
                    
                    segment_data = response.json()

                    for s in segment_data['items']:
                        segment = Segment(
                            key=s['key'],
                            name=s['name'],
                            description=s['description'] if 'description' in s else '',
                            match_type=SegmentMatchType.all,
                            constraints=[],
                        )

                        for rule in s['rules']:
                            for clause in rule['clauses']:
                                constraint = Constraint(
                                    type=ConstraintComparisonType.string,
                                    property=clause['attribute'],
                                    operator=clause['op'],
                                    value=clause['values'][0],
                                )
                                segment.constraints.append(constraint)

                        environments[environment].append(segment)
                
                if environment in documents.namespaces:
                    documents.namespaces[environment].flags.append(flag)
                    documents.namespaces[environment].segments.extend(environments[environment])
                else:
                    documents.namespaces[environment] = Document(flags=[flag], segments=environments[environment])

        return documents
