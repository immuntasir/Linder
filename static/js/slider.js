var Iterator = function(items) {
    this.index = 0;
    this.items = items;
}

Iterator.prototype = {
    first: function() {
        this.reset();
        return this.next();
    },
    next: function() {
        return this.items[this.index++];
    },
    prev: function() {
        return this.items[this.index--];
    },
    hasNext: function() {
        return this.index < this.items.length;
    },
    hasPrev: function() {
        return this.index >=0;
    },
    reset: function() {
        this.index = 0;
    },
    end: function() {
        this.index = this.items.length - 1;
    },
    each: function(callback) {
        for (var item = this.first(); this.hasNext(); item = this.next()) {
            callback(item);
        }
    }
}


var items = [1, 2, 3];
var iter = new Iterator(items);


function plusDivs(n) {
  console.log(n)
  if (n > 0) {
    if (iter.hasNext()) {
        showDivs(iter.next());
    }
    else {
        iter.reset();
        showDivs(iter.next());
    }
  } 
  else if (n<0) {
    if (iter.hasPrev()) {
        showDivs(iter.prev());
    }
    else {
        iter.end();
        showDivs(iter.prev());
    }
    
  } 
}


function showDivs(n) {
      slideIndex = n
      var x = document.getElementsByClassName("mySlides");
      
      for (i = 0; i < x.length; i++) {
         x[i].style.display = "none";  
      }
      x[slideIndex-1].style.display = "block";  
}    

