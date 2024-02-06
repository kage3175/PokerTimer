class TextObj:
  def __init__(self, font, content = "",position = (0,0), relative = "topleft", color = (0,0,0)) -> None:
    self.content = content
    self.text = font.render(content, True, color)
    self.rect = self.text.get_rect()
    self.position = position
    self.relative = relative
    self.color = color
    self.clicked = False
    if relative == "topleft":
      self.rect.topleft = position
    elif relative == "center":
      self.rect.center = position
    elif relative == "rcenter":
      self.rect.centery = position[0]
      self.rect.right = position[1]
    elif relative == "lcenter":
      self.rect.centery = position[0]
      self.rect.left = position[1]
    elif relative == "topright":
      self.rect.topright = position
  def changePosition(self, relative = "topleft", position = (0,0)):
    self.relative = relative
    if relative == "topleft":
      self.rect.topleft = position
    elif relative == "bottom":
      self.rect.bottom = position
    elif relative == "center":
      self.rect.center = position
    elif relative == "right":
      self.rect.right = position
    elif relative == "left":
      self.rect.left = position
    elif relative == "top":
      self.rect.top = position[1]
      self.rect.centerx=position[0]
    self.position = position
  def getRect(self):
    return self.rect
  def changeColor(self, color):
    self.color = color
  def changeContent(self, font, content = ""):
    self.content = content
    self.text = font.render(content, True, self.color)
    self.rect = self.text.get_rect()
    if self.relative == "topleft":
      self.rect.topleft = self.position
    elif self.relative == "center":
      self.rect.center = self.position
    elif self.relative == "rcenter":
      self.rect.centery = self.position[0]
      self.rect.right = self.position[1]
    elif self.relative == "lcenter":
      self.rect.centery = self.position[0]
      self.rect.left = self.position[1]
    elif self.relative == "topright":
      self.rect.topright = self.position
    elif self.relative == "top":
      self.rect.centerx = self.position[0]
      self.rect.top = self.position[1]
  def getContent(self):
    return self.content
  def getText(self):
    return self.text
  def click(self):
    self.clicked=not self.clicked
  def getPos(self):
    return self.position