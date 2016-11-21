$(document).ready(function(){

    show_diff();

});


function show_diff() {
    console.log('showing diff');
    $.get('get_diff/', {}, function(data){
        original_file = data['original_file'].join('\n');
        new_file = data['new_file'].join('\n');
        diff = data['diff_file'];

        $("#original_file").val(original_file);
        $("#new_file").val(new_file);


        for (i=0; i<diff.length; i++) {
            line = diff[i];
            line_id = 'line_num_' + i;
            line_id_selector = '#' + line_id;
            $("#diff_file").append('<p id=' + line_id + '><\p>');
            $(line_id_selector).text(line);
            change = line.charAt(0);
            if (change == '+') {
                $(line_id_selector).addClass('green');
            }
            if (change == "-") {
                $(line_id_selector).addClass('red');
            }
        }

    });
}
