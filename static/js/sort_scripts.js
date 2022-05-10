window.onload = function () {
    $('.search-form').on('change', 'input[type="number"]', function () {
        console.log(event.target.value);
        var target_href = event.target;

        if (target_href) {
            $.ajax({
                url: "http://127.0.0.1:8000/products/category/0/",

                success: function (data) {
                    $('.search_form').html(data.result);
                    console.log('ajax done');
                },
            });

        }
        event.preventDefault();
    });

    }
