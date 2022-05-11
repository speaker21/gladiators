import tkinter as tk

root = tk.Tk()

canvas = tk.Canvas(root, width=300, height=300)
canvas.pack()

# Note:
# If the images overlap exactly (same position & extent),
# the bottom one will never? get any events.
# Maybe events can be propagated, not sure right now.

fgImg = tk.PhotoImage(master=root, file='media/fg.png')
fgImgId = canvas.create_image(
  80, 80, anchor=tk.NW, image=fgImg
)
canvas.tag_bind(
  fgImgId,
  '<ButtonRelease-1>',
  lambda e: canvas.tag_raise(fgImgId)
)

bgImg = tk.PhotoImage(master=root, file='media/bg.png')
bgImgId = canvas.create_image(
  0, 0, anchor=tk.NW, image=bgImg
)
canvas.tag_bind(
  bgImgId,
  '<ButtonRelease-1>',
  lambda e: canvas.tag_raise(bgImgId)
)

root.mainloop()