class Gadget:
    # Display modes
    ICON = 'icon'
    CHIP = 'chip'

    def __init__(
            self,
            title,
            type_,
            link,
            icon_link,
            display=None,
            height=None,
            width=None,
            preferences=None,
    ):
        """
        A gadget that can extend the event.

        :param title:
                the gadget's title.
        :param type_:
                the gadget's type.
        :param link:
                the gadget's URL. The URL scheme must be HTTPS.
        :param icon_link:
                the gadget's icon URL. The URL scheme must be HTTPS.
        :param display:
                the gadget's display mode. Possible values are:
                    Gadget.ICON - The gadget displays next to the event's title in the calendar view.
                    Gadget.CHIP - The gadget displays when the event is clicked.
        :param height:
                the gadget's height in pixels. The height must be an integer greater than 0.
        :param width:
                the gadget's width in pixels. The width must be an integer greater than 0.
        :param preferences:
                TODO: add when ready
        """

        def check_not_empty(v, name):
            if not v:
                raise ValueError('"{}" can not be empty'.format(name))

        def check_positive_integer(v, name):
            if v is not None and (not isinstance(v, int) or v <= 0):
                raise ValueError('"{}" has to be a positive integer'.format(name))

        check_not_empty(title, 'title')
        check_not_empty(type_, 'type_')
        check_not_empty(link, 'link')
        check_not_empty(icon_link, 'icon_link')

        if display and display not in (Gadget.ICON, Gadget.CHIP):
            raise ValueError('"display" has to be on of Gadget.ICON or Gadget.CHIP')

        check_positive_integer(height, 'height')
        check_positive_integer(width, 'width')

        self.title = title
        self.type_ = type_
        self.link = link
        self.icon_link = icon_link
        self.display = display
        self.height = height
        self.width = width
        self.preferences = preferences or {}
