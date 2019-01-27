from gcsa.gadget import Gadget
from .base_serializer import BaseSerializer


class GadgetSerializer(BaseSerializer):
    type_ = Gadget

    def __init__(self, gadget):
        super().__init__(gadget)

    @staticmethod
    def to_json(gadget):
        res = {
            "title": gadget.title,
            "type": gadget.type_,
            "link": gadget.link,
            "iconLink": gadget.icon_link,
            "preferences": gadget.preferences
        }

        if gadget.width:
            res["width"] = gadget.width
        if gadget.height:
            res["height"] = gadget.height
        if gadget.display:
            res["display"] = gadget.display

        return res

    @staticmethod
    def to_object(json_gadget):
        BaseSerializer.assure_dict(json_gadget)

        return Gadget(
            title=json_gadget['title'],
            type_=json_gadget['type'],
            link=json_gadget['link'],
            icon_link=json_gadget['iconLink'],
            display=json_gadget.get('display', None),
            height=json_gadget.get('height', None),
            width=json_gadget.get('width', None),
            preferences=json_gadget.get('preferences', None)
        )
