> 发出前两篇Python实战的文章之后，有同学和我反映：**你的想法很牛逼，可是我就是看不懂你写的是什么，我Python不熟悉，看起来有点吃力**。我细细一琢磨，这点是个问题。对于熟悉Python的同学，能够看懂我思路，但是对于那些没有Python基础，或者对Python不熟悉的同学，这样直接扔过来，可能会让他们失望而归。所以，这回我弄了一期手把手的实战教程，同时，在文章中遇到的知识点，还会有提供链接。完全对新手有好。

在前两篇Python实战[「用代码来访问1024网站」](https://mp.weixin.qq.com/s?__biz=MzI2ODYwNjE5NQ==&mid=2247483753&idx=1&sn=8df6c2a190201826f6f860659ad4af9e&chksm=eaec4ef5dd9bc7e39e8d48134795f6c0173c4614c615d0dcaaa38d937f4394aee77a978d70b1#rd)和[「用Scrapy编写“1024网站种子吞噬爬虫”」](https://mp.weixin.qq.com/s?__biz=MzI2ODYwNjE5NQ==&mid=2247483776&idx=1&sn=50609d6dcf9c2c2fd80addb2d190fff2&chksm=eaec4e1cdd9bc70ab1ef74f7ae64bb3d619c9a09f2e2f0a676bbac33aa66260b7d566cb85154#rd)收到了大家的一致好评，可能文章写得比较匆忙，有些术语可能对于Python的初级玩家不是很好理解。所以，我特别准备了一下，用超级详细的解说，细化到每一步，提供查询链接等方法，为Python初级玩家，Python小白和对Scrapy框架不熟悉的同学，的制作了这篇手把手Python实战教程：用Scrapy爬取下载达盖尔社区的资源。

好了，废话不多说，学习代码就是要学以致用的。不能写了一遍代码就让代码吃灰。下面就跟我一起来搞吧。

小草网站是个好网站，我们这次实战的结果，是要把“达盖尔旗帜”里面的帖子爬取下来，将帖子的图片保存到本地，同时将帖子的一些相关信息，写入到本地的MongoDB中。这么乍一听，感觉我们做的事情好像挺多的，别慌，我带你慢慢的一步一步来搞起，问题不是很大。

### 手把手 Step By Stefp
Scrapy可以通过pip来安装:
```bash
$ pip install scrapy
```
接下来，我们去事先建好的工程目录里面，创建Scrapy的项目。这里，我们先看一下Scrapy的命令行怎么用，输入`$ scray -help`出来

![scrapy帮助文档](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs01.png)

看到，创建scrapy的工程的命令是`$ scrapy startproject <name>`创建完的结果如下：

![创建工程成功](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs002.png)

OK，这个时候，我们的目录内容变成了如下结构：

![工程结构目录](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs003.png)

下一步就是创建我们的爬虫，还是依靠Scrapy本身自带的命令来创建。输入Scrapy自带四种爬虫模板：**basic**，**crawl**，**csvfeed**和**xmlfeed**四种。我们这里选择basic。
```
$ scrapy genspider --template=basic superspider bc.ghuws.men
```
创建成功，会出现以下提示：

![创建爬虫](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs004.png)

这时候我们的工程目录就变成了这个样子：

![有了爬虫的工程目录](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs005.png)

看到我们的工程里面多了一个spiders文件夹，里面有一个`superspider.py`文件，这个就是我们这次程序的主角。我们来看，这个可爱的小虫子刚生下来是长这个样子的：

![爬虫](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs006.png)

这里呢，就简单说一下：
- **name** - 是咱们的爬虫名字，这个主要是在运行爬虫的时候会用到。
- **allowed_domains** - 是在scrapy自带的OffsiteMiddleware中用到的。Scrapy默认会开启OffsiteMiddleware插件，不在此允许范围内的域名就会被过滤，而不会进行爬取。
- **start_urls** - 爬虫开始爬取的url。
- **parse()方法** - 这个就是处理请求结果的。我们具体的爬虫逻辑大部分就是在这里写。

好了，废话不多说，既然start_urls是用来做爬虫开始爬取的第一个url，那么我们就应该把这里面的数值换成达盖尔社区的地址，然后我们看一下在`parse()`里面返回的值是什么。运行方法，就是输入`$ scrapy crawl superspider`指令即可：

![爬虫v0.1](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs007.png)

![response对象](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs008.png)

![response对象的body](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs009.png)

我们看到，这个response是一个HtmlResponse类，它里面的text属性，里面的字符串就是网页的html文件。OK，这一步结束之后，我们下一步就想办法怎样能够解析html网页了。Scrapy是提供了html对象的解析的，它有一个selector类，可以解析html，同时，里面还支持xpath语法的查找和css的查找。但是这个个人感觉不是很好用，我推荐用BeautifulSoup4库。安装方法只需要`$ pip install beautifulsoup4`。我们这里需要用这个来解析html，所以讲BeautifulSoup4导进来，在解析，然后我们就会得到一个beasutifulsoup对象。之后，我们就要在这个对象里面寻找我们需要解析的对象。

![BeautifulSoup的对象](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs010.png)

![bs解析](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs011.png)

目前网页已经解析好了，下一步就是要在html文件中，找到每一个帖子的信息。我们回头来看html文件的源码，可以看到，每一个帖子其实都是在一个`<tr>`tag里面，其实我们需要的东西，就是下图红色框框里面圈的`<a>`tag。

![html页面](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs012.png)

这里，我们发现，每一个帖子的链接入口，也就是`<a>`tag是有两个特性，一个是有id值，另一个是有`href`值。所以，我们要针对soup对象，调用`find_all()`方法来寻找有特定内容的所有标签。

![抓取所有的 a 标签](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs013.png)

![a 标签结果](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs014.png)

我们得到了一个 `a_list`结果，这是一个list对象，长度102。在这些数据中，有些结果是我们不要的，比如000到007位置的这几个数据，他们在网页中对应的是版规之类的帖子信息，和我们想要的东西不一样，所以，在拿到这个`a_list`数据，我们需要进行一下筛选。

筛选的过程必不可少，筛选的方法有很多种，我们这里就做的简单一点，只选取18年的帖子。为什么会是18年的帖子啊？少年你看，这一列href的值：

![href的区别](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs015.png)

第二个数字“1805”，应该就是“年份+月份”。如果不信，则可以跳到比如论坛100页，看到的是16年3月份的帖子，这里面随便检查一个连接的href值，是“1603”。这就印证了我们的想法是正确的。好，按照这个筛选18年的帖子的思路，我们来筛选一下`a_list`。

![筛选结果diamante](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs016.png)

![筛选完的结果](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs017.png)

看到打印的结果却是是18年的帖子。但是目前的href并不是帖子真正的url。真正的url应该长这个样子：
```html
http://bc.ghuws.men/htm_data/16/1805/3126577.html
```
所以，我们这里得进行拼接。对比上面的url，我们目前只有后半部分，前半部分其实是社区网站的root url。那么我们在settings.py文件里面添加一个`ROOT_URL`变量，并将这个变量导入到我们的spider中即可。代码就变成了这样。为了方便，咱们还可以把帖子的id，也就是`.html`前面的那个数字也摘出来，方便日后使用。

![拼凑出帖子地址](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs018.png)

目前为止，我们拿到了帖子的id和帖子的url。我们的最终目的是要下载图片，所以，我们得让爬虫去按照帖子的url去爬取他们。爬虫需要进入第二层。这里，我们需要使用`yield`函数，调用`scrapy.Request`方法，传入一个callback，在callback中做解析。

![二级爬虫](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs019.png)

现在我们已经进入了每一个帖子的内部，我们现在还没有拿到的信息有帖子的标题和帖子的图片。还是和parse()的步骤一样，这个时候，我们就该分析帖子的html文件了。
我们先找标题。看到html文件中，标题对应的是一个`<h4>`标签。

![post的html](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs020.png)

那这就简单了，我们只需要找到所有的`<h4>`标签，然后看标题是第几个就好。接下来是图片了。每个帖子用的图床都不一样，所以图片部分，我们先来看一下结构：

![图片的标签1](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs021.png)

![图片的标签2](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs022.png)

大概就是这两种，我们看到，图片的标签是`<input>`，关键点就在`type=image`上面，所以我们尝试着看看能不能根据这个来找到图片的地址。

![二级爬虫完成](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs023.png)

我们简单测试一下，看看运行效果：

![爬取帖子页面的图片运行效果](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs024.gif)

完全没有问题，看着好爽。这时候，我们看结果，会发现，我们抓取到的image，会有一两个的图床是不一样的。

![运行结果（部分）](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs025.png)

打开也会看到这个图片，里面的内容也和其他的图片不一样，并且这个图片不是我们想要的。所以，这里我们得做一下过滤。我这里的方法就是要从找到的`image_list`里面，把少数图床不一样的图片url给过滤掉。一般看来，都是找到的第一个图片不是我们想要的，所以我们这里只是判断一下第一个和第二个是否一样就可以。

![筛选图片](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs026.png)

这样打印出来的结果就没有问题喽。

哈哈，现在我们已经拿到了帖子的id，标题，帖子的url地址，还有帖子里面图片的url地址。离我们的目标又近了一步。我之前说过，我们的目标是要把每张图片都保存在本地，目前我们只是拿到了每张图片的url。所以，我们需要把图片都下载下载下来。

其实，当拿到图片的URL进行访问的时候，通过http返回的数据，虽然是字符串的格式，但是只要将这些字符串保存成指定的图片格式，我们在本地就可以按照图片的解析来打开。这里，我们拿到帖子的`image_list`，就可以在yield出一层请求，这就是爬虫的第三层爬取了。

![红框框的很关键](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs027.png)

同时，在第三层爬虫里面，我们还需要将访问回来的图片保存到本地目录。那么代码就长这个样子：

![三级爬虫](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs028.png)

在上面第二次爬取函数的最后，有个地方需要注意一下，就是上图中红色框框圈出来的地方。这里需要加上`dont_filter=True`。否则就会被Scrapy给过滤掉。因为图床的地址，并未在我们刚开始的`allow_domain`里面。加上这个就可以正常访问了。

这样运行一遍，我们的本地目录里面就会有保存好的下载照片了。

![图片保存节选](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs029.png)

![本地文件夹保存的下载好的图片](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs030.png)

我们还有个问题，就是我们需要将每个帖子的信息（*id，title，url，*和*image*）都保存到本地的数据库中。这个该怎么做？

别慌，这个其实很简单。

首先，我们得针对每个帖子，建立一个Scrapy的item。需要在items.py里面编写代码：

![scrapy item](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs031.png)

写好之后，我们需要在爬虫里面引入这个类，在第二层解析函数中，构建好item，最后yield出来。这里，yield出来，会交给Scrapy的`pipeline`来处理。

![生成item](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs032.png)

yield出来的item会进入到pipeline中。但是这里有个前提，就是需要将pipeline在settings.py中设置。

![将pipeline添加到settings里面](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs033.png)

pipeline中我们先打印帖子的id，看看数据能不能够传入到这里

![pipeline](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs034.png)

运行：

![pipeline完美运行](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs035.png)

看到数据是完全可以过来的，而且在Scrapy的log中，会打印出来每一个item里面的信息。

我们如果想把数据保存到**MongoDB**中，这个操作就应该是在pipeline中完成的。Scrapy之所以简历pipeline就是为了针对每个item，如果有特殊的处理，就应该在这里完成。那么，我们应该首先导入`pymongo`库。然后，我们需要在pipeline的`__init__()`初始化进行连接数据库的操作。整体完成之后，pipeline应该长这个样子：

![pipeline代码](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs036.png)

那么我们来测试一下数据是否能够存入到MongoDB中。首先，在terminal中，通过命令`$ sudo mongod`来启动MongoDB。

![启动MondoDB](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs037.png)

那么运行一下，看一下效果：

![MongoDB里面保存的数据](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs038.png)

可以看到，左侧，有名为`Daguerre`的数据库，里面有名为`postTable`的表，而且我们的数据成功的写入了数据库中。数据的格式如图所展示，和我们预期的结果是一样的。

目前为止，我们完成了：从一页page中，获得所有帖子的url，然后进入每个帖子，再在帖子中，爬取每个帖子的图片，下载保存到本地，同时把帖子的信息存储到数据库中。

但是，这里你有没有发现一个问题啊？我们只爬取了第一页的数据，那如何才能爬取第二页，第三页，第N页的数据呢？

别慌，只需要简单的加几行代码即可。在我们的spider文件中的`parse()`方法地下，加一个调用自己的方法即可，只不过，传入的url得是下一页的url，所以，我们这里得拼凑出下一页的url，然后再次调用`parse()`方法即可。这里为了避免无限循环，我们设定一个最大页数`MAX_PAGES`为3，即爬取前三页的数据。

![爬取下一个页面](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs039.png)

OK，这样就完事儿了，这个达盖尔旗帜的爬虫就写好了。我们运行一下瞅瞅效果：

![Boom，运行效果爆炸](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs040.gif)

是不是非常的酷炫？再来看看我们的运行结果：

![爬虫运行结果1](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs041.png)

![爬虫运行结果2](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs042.png)

![爬虫运行结果3](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs043.png)

**只能说，战果累累，有图有真相。**

其实，这个程序，可以加入middleware，为http请求提供一些Cookie和User-Agents来防止被网站封。同时，在settings.py文件中，我们也可以设置一下`DOWNLOAD_DELAY`来降低一下单个的访问速度，和`CONCURRENT_REQUESTS`来提升一下访问速度。

![DOWNLOAD_DELAY](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs044.png)

![CONCURRENT_REQUESTS](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs045.png)

就像之前EpicScrapy1024项目里面一样。喜欢的同学，可以去借鉴那个项目代码，然后融会贯通，自成一派，爬遍天下网站，无敌是多么的寂8 寞~~~~


好啦，能看到这里说明少年你很用心，很辛苦，是一个可塑之才。

废话不说，看到这里是有奖励的。关注“**皮克啪的铲屎官**”，回复“**达盖尔**”，即可获得项目源码和说明文档。同时，可以在下面的菜单中，找到“**Python实战**”按钮，能够查看以往文章，篇篇都非常精彩的哦~

扯扯皮，我觉得学习编程最大的动力就是爱好，其实干什么事情都是。爱好能够提供无线的动力，让人元气满满的往前冲刺。代码就是要方便作者，方便大家。写出来的代码要有用处，而且不要吃灰。这样的代码才是好代码。欢迎大家关注我的公众号，“皮克啪的铲屎官”，之后我会退出Python数据分析的内容，可能会结合量化交易之类的东西。

最后，来贴一张达盖尔的图片，纪念一下这位为人类做出杰出贡献的人。

![达盖尔本尊](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs046.jpg)


#### 推荐阅读：
[【Python实战】用Scrapy编写“1024网站种子吞噬爬虫”，送福利](https://mp.weixin.qq.com/s?__biz=MzI2ODYwNjE5NQ==&mid=2247483776&idx=1&sn=50609d6dcf9c2c2fd80addb2d190fff2&chksm=eaec4e1cdd9bc70ab1ef74f7ae64bb3d619c9a09f2e2f0a676bbac33aa66260b7d566cb85154#rd)  
[【Python实战】用代码来访问1024网站，送福利](https://mp.weixin.qq.com/s?__biz=MzI2ODYwNjE5NQ==&mid=2247483753&idx=1&sn=8df6c2a190201826f6f860659ad4af9e&chksm=eaec4ef5dd9bc7e39e8d48134795f6c0173c4614c615d0dcaaa38d937f4394aee77a978d70b1#rd)


![关注公众号“皮克啪的铲屎官”，回复“达盖尔”就可以获得惊喜](https://github.com/SwyftG/DaguerreSpider/blob/master/image/sbs047.jpg)