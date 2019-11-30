# 谷歌图片爬虫/GoogleImageSpider
原理
##### 首先我们把要查询的内容作为参数放在url里发送，就像这样："https://www.google.com/search?q=Hamburger&source=lnms&tbm=isch" 。然后你会得到一个HTML响应文件。
##### 进入第二步，谷歌的图片不是以明显的Ajax形式加载的。它是通过运行一个javascript脚本来向服务器请求图片资源。我通过Fiddler找到了这个javascript脚本的url：https://www.google.com/search?ei=jrviXfz3CI3nsAfz16L4Ac&q=Hamburger&tbm=isch&ved=0ahUKEwk89vbSzpLmAhWNMwKHfOrCD8QuT0ISSgB&ijn=1&start=100&asearch=ichunk&async=_id:rg_s,_pms:s,_jsfs:Ffpdje,_fmt:pc

##### 在这个url里，ei和ved是藏在第一步获得的HTML文件里的两个参数，可以找到；ijn和start就和Ajax很像了，一个是页码，一个是起始位置。最后两个参数不管你搜什么内容都是不变的，但是并不可少，否则请求会失败。
##### 这个请求的响应体是就个javascript，里面有一张存有100个元素的列表，也就是100张图片的信息（在浏览器显示的顺序编号、url等）。从里面取出图片的url进行访问，拿到响应体再写入文件里就完成了。

Principle
##### Firstly, the content to be searched is put in the URL and sent, like this: "https://www.google.com/search?q=Hamburger&source=lnms&tbm=isch". Then the HTML response body is generated.
##### For the next step, should first know that images on Google are not loaded in the form of Ajax. Instead, it currently requests images from the server by running a javascript. I used Fiddler and found the URL corresponding to the javascript: https://www.google.com/search?ei=jrviXfz3CI3nsAfz16L4Ac&q=Hamburger&tbm=isch&ved=0ahUKEwk89vbSzpLmAhWNMwKHfOrCD8QuT0ISSgB&ijn=1&start=100&asearch=ichunk&async=_id:rg_s,_pms:s,_jsfs:Ffpdje,_fmt:pc

##### In this URL, 'ei' and 'ved' are two parameters that can be found in the HTML document from the first step. 'ijn' and 'start' just resemble Ajax. ijn is the page number and 'start' is the starting position. The last two parameters are constant everytime you search. But they are essential and can't be left out or the request will fail.
##### The reponse of this request is a javascript. Inside it, there is a 100-element list, in which information (the number of the order that the image is shown on the browser, url, etc.). URL is taken from the list and the request is sent. The response body is got and written in a file. Everything is done.  
