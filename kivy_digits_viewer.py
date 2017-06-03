#!/usr/bin/python
from sys import argv, exit
from kivy.app import App
from kivy.graphics import Color, Rectangle
from datactrl import DataController

class DigitsViewerApp(App):
  def __init__(self, **kwargs):
    super(DigitsViewerApp, self).__init__(**kwargs)
    self.kwargs = kwargs
    self.curidx = 0

  def dealwith_go(self):
    dc      = self.kwargs['data']
    idx_new = int(self.root.ids.input_id.text)
    if dc.sample_by_key(idx_new) is not None:
      self.curidx = idx_new
      self.clear_canvas()
      self.refresh_render(dc, idx_new)

  def dealwith_prev(self):
    dc      = self.kwargs['data']
    idx_new = self.curidx - 1
    if dc.sample_by_key(idx_new) is not None:
      self.curidx = idx_new
      self.clear_canvas()
      self.refresh_render(dc, idx_new)

  def dealwith_next(self):
    dc      = self.kwargs['data']
    idx_new = self.curidx + 1
    if dc.sample_by_key(idx_new) is not None:
      self.curidx = idx_new
      self.clear_canvas()
      self.refresh_render(dc, idx_new)

  def clear_canvas(self):
    self.root.ids.canvas_digits.canvas.clear()

  def refresh_render(self, dc, index):
    if type(dc) == DataController and type(index) == int:
      str_info_sample           = 'Total Sample: %d'%(dc.count_sample())
      str_info_judged           = 'Total Judged: %d'%(dc.count_judged())
      str_info_completion_rate  = 'Completion Rate: %.2f%%'%(100.0 * dc.completion_rate())
      str_info_precision        = 'Precision: %.2f%%'%(100.0 * dc.precision())

      self.root.ids.info_sample.text      = str_info_sample
      self.root.ids.info_judged.text      = str_info_judged
      self.root.ids.info_completion.text  = str_info_completion_rate
      self.root.ids.info_precision.text   = str_info_precision

      data  = dc.sample_by_key(index)
      if data is not None:
        str_info_cur_sample = 'Current Sample ID: %d'%(index)
        str_info_cur_expect = 'Expect Result: %d'%(data[1])
        str_info_cur_judged = 'Judged Result: %d'%(data[2])

        self.root.ids.info_cur_sample.text  = str_info_cur_sample
        self.root.ids.info_cur_expect.text  = str_info_cur_expect
        self.root.ids.info_cur_judged.text  = str_info_cur_judged

        self.refresh_canvas(data[0])
    else:
      raise TypeError('please provide DataController & index')

  def refresh_canvas(self, data_paint):
    with self.root.ids.canvas_digits.canvas:
      cvs_width, cvs_height = self.root.size
      cvs_width             = int(cvs_width * 0.6)
      scale, point_colors   = data_paint
      scale_x, scale_y      = scale
      scale_rate            = 0.8
      point_size            = int(scale_rate * float(min(cvs_width, cvs_height)) / float(max(scale_x, scale_y)))
      start_x, start_y      = int((cvs_width - scale_x * point_size) / 2), int((cvs_height + scale_y * point_size) / 2)

      for y in range(scale_y):
        for x in range(scale_x):
          p_color     = point_colors[y * scale_y + x]
          cur_posi    = (start_x + point_size * x, start_y - point_size * y)

          color_r     = float(p_color + 45.0) / 300.0
          color_g     = float(p_color + 45.0) / 300.0
          color_b     = float(p_color + 45.0) / 300.0
          color_a     = 0.8

          Color(color_r, color_g, color_b, color_a)
          Rectangle(pos = cur_posi, size = (point_size, point_size))

  def on_start(self):
    self.refresh_render(self.kwargs['data'], self.curidx)

def main():
  if len(argv) != 4:
    exit(1)
  fn_image        = argv[1]
  fn_label_expect = argv[2]
  fn_label_judged = argv[3]

  dc  = DataController(fn_image, fn_label_expect, fn_label_judged)
  DigitsViewerApp(data = dc).run()

if __name__ == '__main__':
  main()
