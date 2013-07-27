$(function() {

$('#gh-repo-events').on('submit', function(e) {
    e.preventDefault();
    var $form = $(this),
        $graph = $form.next('.graph');

    $.ajax({
        url: $form.attr('action'),
        type: 'POST',
        data: $form.serialize()
    }).done(function(response) {
        $graph.empty().append($('<img>').attr('src', response));
    }).error(function() {
        $graph.text('Failed to render graph!');
    }).always(function() {
        $form.find('input').prop('disabled', false);
    });

    // Loading feedback
    $graph.html('Loading&hellip;');
    $form.find('input').prop('disabled', true);
});

});
