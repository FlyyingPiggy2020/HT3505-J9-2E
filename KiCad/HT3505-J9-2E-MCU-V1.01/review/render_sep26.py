from pathlib import Path
import urllib.request
import pypdfium2 as pdfium
root=Path(__file__).resolve().parent
url='https://www.magntek.com.cn/upload/pdf/202312/MT6701_Rev.1.8_%E4%B8%AD%E6%96%87%E7%89%88.pdf'
data=urllib.request.urlopen(url,timeout=30).read()
(root/'MT6701-rev1.8-cn.pdf').write_bytes(data)
d=pdfium.PdfDocument(data)
d[19].render(scale=1.7).to_pil().save(root/'mt6701-i2c.png')
print('Rendered datasheet I2C reference.')
