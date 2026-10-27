(function(){
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var els=document.querySelectorAll('.reveal');
  if(!('IntersectionObserver' in window)||reduce){els.forEach(function(e){e.classList.add('in')});}
  else{var io=new IntersectionObserver(function(l){l.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{threshold:.12});els.forEach(function(e){io.observe(e)});}
  /* the pinned phone shows the screen of the chapter that is crossing the middle of the viewport */
  var screens=document.querySelectorAll('.screen'),chapters=document.querySelectorAll('.chapter[data-step]');
  if(!screens.length||!('IntersectionObserver' in window)||reduce)return;
  function show(n){screens.forEach(function(s){var on=s.getAttribute('data-screen')===String(n);s.classList.toggle('is-on',on);s.setAttribute('aria-hidden',on?'false':'true');});}
  show(0);
  var so=new IntersectionObserver(function(l){l.forEach(function(e){if(e.isIntersecting)show(e.target.getAttribute('data-step'));})},{rootMargin:'-45% 0px -45% 0px',threshold:0});
  chapters.forEach(function(c){so.observe(c)});
})();
