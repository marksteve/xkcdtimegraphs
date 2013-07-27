$(function() {

$('#gh-repo-events').on('submit', function(e) {
    e.preventDefault();
    var $form = $(this);
    $.ajax({
        url: $form.attr('action'),
        type: 'POST',
        data: $form.serialize()
    }).done(function(response) {
        $form.next('.graph').empty().append(
            $('<img>').attr('src', response)
        );
    }).error(function() {
        alert('Oops!');
    });
});

});
