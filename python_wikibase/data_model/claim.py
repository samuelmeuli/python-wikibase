from .data_type import marshal_data_type, unmarshal_data_value
from ..base import Base


class Claims(Base):
    def __init__(self, py_wb, api, language):
        super().__init__(py_wb, api, language)
        self.claims = {}
        self.item_id = None

    def unmarshal(self, item_id, claims):
        self.item_id = item_id

        for prop_id, prop_claim_dicts in claims.items():
            for claim_dict in prop_claim_dicts:
                claim = self.py_wb.Claim().unmarshal(self.item_id, claim_dict)
                self._add_locally(claim)
        return self

    def _add_locally(self, claim):
        prop_id = claim.property.entity_id
        if prop_id in self.claims:
            self.claims[prop_id].append(claim)
        else:
            self.claims[prop_id] = [claim]

    def _create_and_add(self, prop, value, snak_type):
        # Create claim
        prop_id = prop.entity_id
        if value:
            value_marshalled = marshal_data_type(value)
            r = self.py_wb.api.claim.add(
                self.item_id, prop_id, value_marshalled, snak_type=snak_type
            )
        else:
            r = self.py_wb.api.claim.add(self.item_id, prop_id, None, snak_type=snak_type)

        # Save claim in Claims
        new_claim = self.py_wb.Claim().unmarshal(self.item_id, r["claim"])
        self._add_locally(new_claim)
        return self

    def add(self, prop, value):
        return self._create_and_add(prop, value, "value")

    def add_no_value(self, prop):
        return self._create_and_add(prop, None, "novalue")

    def add_some_value(self, prop):
        return self._create_and_add(prop, None, "somevalue")

    def remove(self, claim):
        # Parameter validation
        if not isinstance(claim, Claim):
            raise ValueError(f'"claim" parameter must be instance of Claim class')

        # Delete claim
        self.py_wb.api.claim.remove(claim.claim_id)

        # Remove claim from Claims
        prop_id = claim.property.entity_id
        self.claims[prop_id] = [c for c in self.claims[prop_id] if not c.claim_id == claim.claim_id]
        if len(self.claims[prop_id]) == 0:
            del self.claims[prop_id]

        return self

    def to_dict(self):
        return self.claims

    def to_list(self):
        claim_list = []
        [claim_list.extend(claims) for prop, claims in self.claims.items()]
        return claim_list


class Claim(Base):
    def __init__(self, py_wb, api, language):
        super().__init__(py_wb, api, language)
        self.claim_id = None
        self.item_id = None
        self.property = None
        self.rank = None
        self.snak_type = None
        self.value = None

    def __eq__(self, other):
        return self.claim_id == other.claim_id

    def unmarshal(self, item_id, claim_data):
        main_snak = claim_data["mainsnak"]
        self.claim_id = claim_data["id"]
        self.item_id = item_id
        self.property = self.py_wb.Property()
        self.property.entity_id = main_snak["property"]
        self.rank = claim_data["rank"]

        # Parse snak type and value (if snak type is "value")
        self.snak_type = main_snak["snaktype"]
        if self.snak_type == "value":
            self.value = unmarshal_data_value(self.py_wb, main_snak)
        return self
