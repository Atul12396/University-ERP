(function($) {
    $(document).ready(function() {
        function toggleFields() {
            const status = $('#id_hostel_status').val();
            if (status === 'Allocated') {
                $('#id_hostel').parent().show();
                $('#id_block').parent().show();
                $('#id_room').parent().show();
            } else {
                $('#id_hostel').parent().hide();
                $('#id_block').parent().hide();
                $('#id_room').parent().hide();
            }
        }

        // Initial call to toggle fields
        toggleFields();

        // Bind change event to the hostel_status field
        $('#id_hostel_status').change(function() {
            toggleFields();
        });
    });
})(django.jQuery);
