// this is how $.widget.bridge works in the widget factory.  it works standalone.


// create a JavaScript "widget" object
var widget = function( options, element ){
    this.options = options;
    this.element = element;
    this._init();
};

widget.prototype = {
    
    // if you call your widget without any args or pass in a hash
    // after it has already been initialized, bridge relies on
    // _init and option methods existing.
    _init: function(){
       
    },
    option: function( options, value ){
        
        // change options after initialization
        this.options = $.extend(true, this.options, options);
        
        return this; // make sure to return the object!
    },
    public: function(){
        return "public method";
    },
    _private: function(){
        return "private method";
    }
};

// connect the widget obj to jQuery's API under the "foo" namespace
$.widget.bridge("foo", widget);

// now you can do...
var widget = $("#elem").foo({
    cool: true
});

/*
  which does three things:

  1. checks to see if the object has already been inited.
     if so, automatically calls the _init method.

  2. creates a new widget instance, passing in the options
     hash and the element the widget was initialized upon.

  3. stores the object in the element's $.data cache.
*/

// your widget instance exists in the elem's data
widget.data("foo").element; // => #elem element

// bridge allows you to call public methods...
widget.foo("public"); // => "public method"

// bridge prevents calls to internal methods
widget.foo("_private"); // => #elem element

// bridge prevents method calls to uninitialized widgets
// thrown error introduced in v1.8.5
$("#bar").foo("public"); // => "cannot call methods on 'foo' prior to initialization..."

// bridge prevents calls to non-existing methods
// thrown error introduced in v1.8.5
$("#bar").foo("hai"); // => "no such method 'hai' for foo instance"

// if you attempt to re-initialize the widget...
widget.foo({ cool:false });

/*
   bridge will take the EXISTING instance, run the "options"
   method to update any new options that were passed in,
   and automatically fire the _init() method.
  
   for this to work correctly, bridge makes two assumptions:
   
     1. your object has an "option" and "_init" method.
     2. your "options" method returns the current instance.
        "options" is called first, and immediately chained to
        that is "_init", so "option" must return an object with
        an _init method.
*/
