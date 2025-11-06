import unittest
import io
from main import get_currencies
import requests

class TestStreamWrite(unittest.TestCase):


  def setUp(self):
    self.nonstandardstream = io.StringIO()


    try:
      self.get_currencies = get_currencies(['USD'],
                                         url="https://",
                                         handle=self.nonstandardstream)
    except:
      pass
    # self.trace = trace(get_currencies, handle=self.nonstandardstream)


  def test_writing_stream(self):
      stream_content = self.nonstandardstream.getvalue()
      self.assertNotEqual = (stream_content, "", 'Поток пуст')
      self.assertIs = ("Ошибка при запросе к API", stream_content)

  def tearDown(self):
    del self.nonstandardstream



if __name__ == '__main__':
    """Запуск всех тестовых случаев, определенных в классе TestBinTree."""
    unittest.main()
