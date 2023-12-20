class ActiveColorPair():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.colorf = (255, 255, 255, 255)
            cls._instance.colorb = (0, 0, 0, 255)
        return cls._instance
    
    def set_color_f(self, color):
        self._instance.colorf = color

    def set_color_b(self, color):
        self._instance.colorb = color

    def swap_colors(self):
        temp = self._instance.colorf
        self._instance.colorf = self._instance.colorb
        self._instance.colorb = temp
