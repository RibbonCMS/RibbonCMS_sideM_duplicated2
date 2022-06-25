from PIL import Image, ImageDraw, ImageFilter, ImageFont


def paste_icon_image(
            base_img, 
            icon_img, 
            icon_w, 
            icon_h, 
            icon_pos_h,
            icon_pos_w=None,
        ):
    mask = Image.new("L", icon_img.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse(
            (0,0, icon_img.size[0], icon_img.size[1]), 
            fill=255
        )
    mask = mask.filter(ImageFilter.GaussianBlur(1))
    icon_img.putalpha(mask)
    paste_img = Image.new(
            "RGB", 
            icon_img.size, (255,255,255)
        )
    paste_img.paste(
            icon_img, 
            mask=icon_img.convert("RGBA").split()[-1]
        )
    w, h = icon_w, icon_h
    if icon_pos_w is None:
        icon_pos_w = int(base_img.size[0] / 2 - w/2)
    base_img.paste(
            paste_img.resize((w, h), resample=Image.BICUBIC), 
            (icon_pos_w, icon_pos_h),
        )
    return base_img


def is_text_size_ok(draw, font, text, base_img_width, side_padding, text_padding=0):
    return draw.textsize(text, font=font)[0] + text_padding < base_img_width - side_padding

def add_centered_text(
            base_img, 
            text, 
            font_path, 
            font_size, 
            font_color, 
            height, 
            side_padding, 
            stroke_width=0
        ):
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(base_img)
    
    if not is_text_size_ok(draw, font, text, base_img.size[0], side_padding):
        while not is_text_size_ok(draw, font, text+'…', base_img.size[0], side_padding):
            text = text[:-1]
        text = text + '…'

    draw.text(
            ((base_img.size[0] - draw.textsize(text, font=font)[0]) / 2, height), 
            text, 
            font_color, 
            font=font, 
            stroke_width = stroke_width,
        )

    return base_img

def add_lefted_text(
            base_img, 
            text, 
            font_path, 
            font_size, 
            font_color, 
            position,
            side_padding, 
            stroke_width=0
        ):
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(base_img)
    
    if not is_text_size_ok(draw, font, text, base_img.size[0], side_padding, text_padding=position[0]):
        while not is_text_size_ok(draw, font, text+'…', base_img.size[0], side_padding, text_padding=position[0]):
            text = text[:-1]
        text = text + '…'

    draw.text(
            (position[0], position[1]), 
            text, 
            font_color, 
            font=font, 
            stroke_width = stroke_width,
        )

    return base_img

