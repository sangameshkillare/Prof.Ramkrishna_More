(function($) {
    $(document).ready(function() {
        function filterSubDepartments() {
            var dept_id = $('#id_department').val();
            $('#id_subdepartment option').each(function() {
                var subDeptOption = $(this);
                if (!subDeptOption.val()) return; // skip the empty one

                var parentId = subDeptOption.text().split(' - ')[0];
                if (dept_id && parentId !== $('#id_department option:selected').text()) {
                    subDeptOption.hide();
                } else {
                    subDeptOption.show();
                }
            });
        }

        $('#id_department').change(filterSubDepartments);
        filterSubDepartments();  // Initial call
    });
})(django.jQuery);
