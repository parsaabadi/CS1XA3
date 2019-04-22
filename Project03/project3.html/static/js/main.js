function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

$("#begingame").click(function(event){
  event.preventDefault();
  var date = new Date();
        date.setTime(date.getTime() + (1*24*60*60*1000));
  document.cookie = "id_num = '';curr_scores = 0;total_attempt=0;expires = "+date.toUTCString();
  makeAjaxRequest();
});
function makeAjaxRequest() {
  $.ajax({
      url: '/countrycapital/spellgame/',
      type: 'POST',
      data: JSON.stringify({'roundnumber': 1, 'totalattemptleft': 3, 'curr_score':0}),
      contentType: 'application/json',
      success: function(data){
        $("html").html(data);
      }
  });
}

$("#submitans").click(function(event){
  event.preventDefault();
  var val = $("#input").val();
  makeAjaxRequest2(val);
});
function makeAjaxRequest2(val) {
  $.ajax({
      url: '/countrycapital/spellgamenext/',
      type: 'POST',
      data: JSON.stringify({'answer': val,'roundnumber': 1, 'totalattemptleft': 3, 'curr_score':0}),
      contentType: 'application/json',
      success: function(data){
        $("html").html(data);
      }
  });
}