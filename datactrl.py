#!/usr/bin/python
from idxdata import IdxFile

class DataController(object):
  def __init__(self, fn_image, fn_label_expect, fn_label_judged):
    self._idx_image         = IdxFile()
    self._idx_label_expect  = IdxFile()
    self._idx_label_judged  = IdxFile()

    self._idx_image.load_idx_file(fn_image)
    self._idx_label_expect.load_idx_file(fn_label_expect)
    self._idx_label_judged.load_idx_file(fn_label_judged)

    self.__pair_image_label__()
    self.__calculate_rates__()

  def __pair_image_label__(self):
    payload_image         = self._idx_image.payload()
    payload_label_expect  = self._idx_label_expect.payload()
    payload_label_judged  = self._idx_label_judged.payload()

    dict_ret  = {}
    for key in payload_image:
      if key in payload_label_expect:
        dict_ret[key] = [payload_image[key], payload_label_expect[key]]
    for key in dict_ret:
      if key in payload_label_judged:
        dict_ret[key].append(payload_label_judged[key])
      else:
        dict_ret[key].append(-1)
    self._paired_result = dict_ret

  def __calculate_rates__(self):
    count_sample  = len(self._paired_result)
    count_judged  = 0
    count_right   = 0
    for key in self._paired_result:
      if self._paired_result[key][-1] != -1:
        count_judged  += 1
        if self._paired_result[key][-1] == self._paired_result[key][-2]:
          count_right += 1
    self._count_sample    = count_sample
    self._count_judged    = count_judged
    self._count_right     = count_right
    self._completion_rate = float(count_judged) / float(count_sample)
    self._precision       = float(count_right) / float(count_judged)

  def __str__(self):
    summary_status  = 'Counts: %d, %d, %d\tCompletion-Rate:%.2f%%\tPrecision:%.2f%%'%(self._count_sample, self._count_judged, self._count_judged, 100.0 * self._completion_rate, 100.0 * self._precision)
    return '\n'.join([str(self._idx_image.file_header()), str(self._idx_label_expect.file_header()), str(self._idx_label_judged.file_header()), summary_status])

  def count_sample(self):
    return self._count_sample

  def count_judged(self):
    return self._count_judged

  def count_right(self):
    return self._count_right

  def completion_rate(self):
    return self._completion_rate

  def precision(self):
    return self._precision

  def sample_by_key(self, key):
    if not key in self._paired_result:
      return None
    else:
      return self._paired_result[key]
