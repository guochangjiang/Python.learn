

(function(factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD
    define(['jquery'], factory);
  } else if (typeof module === 'object' && module.exports) {
    // CommonJS
    module.exports = factory(require('jquery'));
  } else {
    // Browser globals
    factory(jQuery);
  }
}


(function($) {

  /* Screentime */

  var defaults = {
    fields: [],
    percentOnScreen: '50%',
    reportInterval: 30,
    googleAnalytics: false,
    callback: function(){}
  };
  //console.log(defaults);

  $.screentime = function(options) {
    options = $.extend({}, defaults, options);


    // Convert perecent string to number
    options.percentOnScreen = parseInt(options.percentOnScreen.replace('%', ''), 10);

    var counter = {};
    var cache = {};
    var log = {};
    var looker = null;
    var started = false;
    var universalGA, classicGA;

    if (!options.fields.length) {
      return;
    }
    /*
     * Utilities
     */

    /*
    
     * Methods supported:
     * visibly.onVisible(callback)
     * visibly.onHidden(callback)
     * visibly.hidden()
     * visibly.visibilityState()
     * visibly.visibilitychange(callback(state));
     */

    // funnction to detect window is visible or not

 (function(){window.visibly={q:document,p:undefined,prefixes:["webkit","ms","o","moz","khtml"],props:["VisibilityState","visibilitychange","Hidden"],m:["focus","blur"],visibleCallbacks:[],hiddenCallbacks:[],genericCallbacks:[],_callbacks:[],cachedPrefix:"",fn:null,onVisible:function(i){if(typeof i=="function"){this.visibleCallbacks.push(i)}},onHidden:function(i){if(typeof i=="function"){this.hiddenCallbacks.push(i)}},getPrefix:function(){if(!this.cachedPrefix){for(var i=0;b=this.prefixes[i++];){if(b+this.props[2]in this.q){this.cachedPrefix=b;return this.cachedPrefix}}}},visibilityState:function(){return this._getProp(0)},hidden:function(){return this._getProp(2)},visibilitychange:function(i){if(typeof i=="function"){this.genericCallbacks.push(i)}var t=this.genericCallbacks.length;if(t){if(this.cachedPrefix){while(t--){this.genericCallbacks[t].call(this,this.visibilityState())}}else{while(t--){this.genericCallbacks[t].call(this,arguments[0])}}}},isSupported:function(i){return this.cachedPrefix+this.props[2]in this.q},_getProp:function(i){return this.q[this.cachedPrefix+this.props[i]]},_execute:function(i){if(i){this._callbacks=i==1?this.visibleCallbacks:this.hiddenCallbacks;var t=this._callbacks.length;while(t--){this._callbacks[t]()}}},_visible:function(){window.visibly._execute(1);window.visibly.visibilitychange.call(window.visibly,"visible")},_hidden:function(){window.visibly._execute(2);window.visibly.visibilitychange.call(window.visibly,"hidden")},_nativeSwitch:function(){this[this._getProp(2)?"_hidden":"_visible"]()},_listen:function(){try{if(!this.isSupported()){if(this.q.addEventListener){window.addEventListener(this.m[0],this._visible,1);window.addEventListener(this.m[1],this._hidden,1)}else{if(this.q.attachEvent){this.q.attachEvent("onfocusin",this._visible);this.q.attachEvent("onfocusout",this._hidden)}}}else{this.q.addEventListener(this.cachedPrefix+this.props[1],function(){window.visibly._nativeSwitch.apply(window.visibly,arguments)},1)}}catch(i){}},init:function(){this.getPrefix();this._listen()}};this.visibly.init()})();
   
 
      //  console.log('page is visible');
    

    function random() {
      return Math.round(Math.random() * 2147483647);
    }

    /*
     * Constructors
     */

    function Field(elem) {
      this.selector = elem.selector;
      $elem = this.$elem = $(elem.selector);
      this.name = elem.name;

      this.top = $elem.offset().top;
      this.height = $elem.height();
      this.bottom = this.top + this.height;
      this.width = $elem.width();
    }

    function Viewport() {
      var $window = $(window);

      this.top = $window.scrollTop();
      this.height = $window.height();
      this.bottom = this.top + this.height;
      this.width = $window.width();
    }

    /*
     * Do Stuff
     */
   
function sendGAEvent(field, time) {

      if (universalGA) {
        ga('send', 'event', 'Screentime', 'Time on Screen', field, parseInt(time, 10), {'nonInteraction': true});
      }

      if (classicGA) {
        _gaq.push(['_trackEvent', 'Screentime', 'Time on Screen', field, parseInt(time, 10), true]);
      }

    }
 

    
    function onScreen(viewport, field) {
      var cond, buffered, partialView;

      // Field entirely within viewport
      if ((field.bottom <= viewport.bottom) && (field.top >= viewport.top)) {
        return true;
      }

       // Field bigger than viewport
      if (field.height > viewport.height) {

        cond = (viewport.bottom - field.top) > (viewport.height / 2) && (field.bottom - viewport.top) > (viewport.height / 2);

        if (cond) {
          return true;
        }

      }

      // Partially in view
      buffered = (field.height * (options.percentOnScreen/100));
      partialView = ((viewport.bottom - buffered) >= field.top && (field.bottom - buffered) > viewport.top);

      return partialView;

    }

    function checkViewport() {
      var viewport = new Viewport();

      $.each(cache, function(key, val) {
        if (onScreen(viewport, val)) {
          log[key] += 1;
          counter[key] += 1;
        }
      });

    }

    function report() {

      var data = {};

      $.each(counter, function(key, val) {
        if (val > 0) {
          data[key] = val;
          counter[key] = 0;

          if (options.googleAnalytics) {
            sendGAEvent(key, val);
          }

        }
      });

      if (!$.isEmptyObject(data)) {
        options.callback.call(this, data, log);
      }

    }

/*
     $(window).blur(function(){
          document.title = ‘Inactive’;
     });
     $(window).focus(function(){
          document.title = ‘Active’;
     });

*/

   function startTimers() {

      if (!started) {
        checkViewport();
        started = true;
      }

      looker = setInterval(function() {
        checkViewport();
      }, 1000);

      reporter = setInterval(function() {
        report();
      }, options.reportInterval * 1000);

    }

    function stopTimers() {
      clearInterval(looker);
      clearInterval(reporter);
    }

    $.screentime.reset = function() {
      stopTimers();

      $.each(cache, function(key, val) {
        log[key] = 0;
        counter[key] = 0;
      });

      startTimers();
    }

    function init() {

      $.each(options.fields, function(index, elem) {
        if ($(elem.selector).length) {
          var field = new Field(elem);
          cache[field.name] = field;
          counter[field.name] = 0;
          log[field.name] = 0;
        }
      });

      startTimers();

      visibly.onHidden(function() {
         console.log('page is hidden');
        stopTimers();
      });

      visibly.onVisible(function() {
       console.log('page is visible');
       stopTimers();
        startTimers();
      });

    
    }

    init();

  };

}));
