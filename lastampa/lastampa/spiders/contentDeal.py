import re
# 处理字符串文本内容
def deal_content(content) :
    content = re.sub(r'\s+', ' ', content, re.S|re.M)
    # 去除 script 代码
    # content = re.sub(r"<script>.*?<\/script>", "", content, re.S)
    # 去除 style 代码
    print (1111)
    content = re.sub(r"<style>[\s\S]*?<\/style>", "", content, re.S|re.M)
    # 将 div 标签变为 p 标签
    # content = re.sub(r"<div.*?>", "<p>", content, re.S)
    # content = re.sub(r"</div>", "<p>", content)
    # # 将 p 标签规格化
    # content = content.replace("</p>", "<p>")
    # content = re.sub(r"<p.*?>", "<p>", content)
    # # 将 br 标签变为空格
    # content = re.sub(r"<br.*?>", " ", content)
    # content = content.replace("</br>", " ")
    # # 去除 a 开头的标签
    # content = re.sub(r"<a.*?>", "", content)
    # content = re.sub(r"</a.*?>", "", content)
    # # 去除 b 开头的标签
    # content = re.sub(r"<b.*?>", "", content)
    # content = re.sub(r"</b.*?>", "", content)
    # # # 去除 e 开头的标签
    # # content = re.sub(r"<e.*?>", "", content)
    # # content = re.sub(r"</e.*?>", "", content)
    # # # 去除 f 开头的标签
    # # content = re.sub(r"<f.*?>", "", content)
    # # content = re.sub(r"</f.*?>", "", content)
    # # 去除 i 开头的标签
    # content = re.sub(r"<i.*?>", "", content)
    # content = re.sub(r"</i.*?>", "", content)
    # # # 去除 l 开头的标签
    # # content = re.sub(r"<l.*?>", "", content)
    # # content = re.sub(r"</l.*?>", "", content)
    # # 去除 s 开头的标签
    # # content = re.sub(r"<s.*?>", "", content)
    # # content = re.sub(r"</s.*?>", "", content)
    # # 去除 t 开头的标签
    # content = re.sub(r"<t.*?>", "", content)
    # content = re.sub(r"</t.*?>", "", content)
    # # 去除 u 开头的标签
    # content = re.sub(r"<u.*?>", "", content)
    # content = re.sub(r"</u.*?>", "", content)
    # # 去除多余的空格
    # content = re.sub(r"\n+", "\n", content)
    # content = re.sub(r"\t+", "\t", content)
    return content
    