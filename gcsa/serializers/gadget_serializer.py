from gcsa.gadget import Gadget
from .base_serializer import BaseSerializer


class GadgetSerializer(BaseSerializer):
    type_ = Gadget

    def __init__(self, gadget):
        super().__init__(gadget)

    @staticmethod
    def _to_json(gadget):
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
    def _to_object(json_gadget):
        return Gadget(
            title=json_gadget.get('title', None),
            type_=json_gadget.get('type', None),
            link=json_gadget.get('link', None),
            icon_link=json_gadget.get('iconLink', None),
            display=json_gadget.get('display', None),
            height=json_gadget.get('height', None),
            width=json_gadget.get('width', None),
            preferences=json_gadget.get('preferences', None),
            _serialized=True
        )
