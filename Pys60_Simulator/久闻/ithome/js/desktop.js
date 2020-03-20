function isDesktop(){ 
        var ua = navigator.userAgent.toLowerCase(); 
        if(ua.indexOf('windows') != -1) { 
            return true; 
        } else { 
            return false; 
        } 
    };
	
if(isDesktop()===true)
{
function MenuItem(name,cmd)
{
	this.name=name;
	this.cmd=cmd;
	return this;
};

widget=new function()
{
	this.setNavigationEnabled = function(b)
	{
		
	};
	this.preferenceForKey = function(b)
	{
		
	};
	
	return this;
};
menu = new function()
{
	this.append = function(b)
	{
		
	};
	this.showSoftkeys= function(b)
	{
		
	};
	this.setRightSoftkeyLabel= function(b)
	{
		
	};
	this.setLeftSoftkeyLabel= function(b)
	{
		
	};
	this.remove= function(b)
	{
		
	};
	
	return this;
};
};