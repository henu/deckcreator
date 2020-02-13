from PIL import Image, ImageColor, ImageChops, ImageOps, ImageFont, ImageDraw

from textwrapper import TextWrapper


class Creator():
    
    def __init__(self, style):
        self.card_size = style['card']
        self.title_pos = style['title'][0:2]
        self.title_size = style['title'][2:4]
        self.image_pos = style['image'][0:2]
        self.image_size = style['image'][2:4]
        self.desc_topic_pos = style['description_topic'][0:2]
        self.desc_topic_size = style['description_topic'][2:4]
        self.desc_pos = style['description'][0:2]
        self.desc_size = style['description'][2:4]
        self.title_font = style['title_font']
        self.title_font_size = style['title_font_size']
        self.description_topic_font = style['description_topic_font']
        self.description_topic_font_size = style['description_topic_font_size']
        self.description_font = style['description_font']
        self.description_font_size = style['description_font_size']

    def create_card(self, path, data):
        card = Image.new('RGB', self.card_size)

        # Background
        background = Image.open(data['background'])
        background_tint = data.get('background_tint')
        if background_tint:
            background = self._apply_tint(background, background_tint)
        self._draw_texture(card, background)

        # Image
        image = Image.open(data['image'])
        image = ImageOps.fit(image, self.image_size, Image.BILINEAR)
        card.paste(image, self.image_pos)

        # Title
        self._draw_text(card, data['title'], data['text_color'], self.title_pos, self.title_size, self.title_font, self.title_font_size)

        # Description topic
        self._draw_text(card, data['description_topic'], data['text_color'], self.desc_topic_pos, self.desc_topic_size, self.description_topic_font, self.description_topic_font_size)

        # Description
        self._draw_text(card, data['description'], data['text_color'], self.desc_pos, self.desc_size, self.description_font, self.description_font_size)

        card.save(path)

    def _draw_texture(self, target, texture):
        for x in range(0, texture.size[0], texture.size[0]):
            for y in range(0, texture.size[1], texture.size[1]):
                target.paste(texture, (x, y))

    def _apply_tint(self, img, tint):
        tint = ImageColor.getrgb(tint)
        return ImageChops.multiply(
            img,
            Image.new('RGB', img.size, tint),
        )

    def _draw_text(self, img, text, color, pos, size, font, font_size):
        color = ImageColor.getrgb(color)
        font = ImageFont.truetype(font, size=font_size)

        wrapper = TextWrapper(text, font, size[0])
        wrapped_text = wrapper.wrapped_text()

        draw = ImageDraw.Draw(img)
        draw_pos = pos
        draw.text(draw_pos, wrapped_text, font=font, fill=color)
