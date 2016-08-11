var casper = require('casper').create({
	pageSettings:{
		loadImages:false,
		laodPlugins:false,
		userAgent:'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'
	},
	verbose:true,
	logLevel:"debug",
});

casper.start('http://weixin.sogou.com',function(){
	this.fill('form#searchForm',{
		'query':'vcbeat',
		'type':'1',
	},false);
});

casper.waitForSelector('input.swz2',function(){
	this.click('input.swz2');
});

casper.waitForSelector('div#sogou_vr_11002301_box_0',function(){
	this.click('div#sogou_vr_11002301_box_0');
});

var r = new RegExp('http://mp.weixin.qq.com/.*');

casper.waitForPopup(r,function(){
	this.echo(this.getCurrentUrl());
});

var links = []
var sites = []

casper.withPopup(r,function(){
	links = this.getElementsAttribute('div.weui_media_bd h4.weui_media_title','hrefs');
});

casper.then(function(){
	this.each(links,function(self,link){
		sites.push('http://mp.weixin.qq.com'+link);
	});
	this.each(sites,function(self,site){
		self.thenOpen(site,function(){
			this.echo('content_url:'+this.getCurrentUrl());
			this.echo('title:'+this.fetchText('#activity-name'));
			this.echo('content:'+this.fetchText('#img-content :not(script)'));
			this.waitForResource(/\d+\.png/,function(){
				this.echo('image_url:'+this.getElementsAttribute('#img-content img','src'));
			});
			
		});
	});
});

casper.run();