jQuery(document).ready(function($) {
    $('section#main').hide();
    $('body').append('<div class="loading">carregando...</div>');

    $.getJSON(jsonUrl, function(data) {
        data.sort(function(a,b) {
            return b.date_posted - a.date_posted;
        });

        var maxItems = 20;
        $.each(data, function (i, item) {
            generateContent(i, item);
            if (i >= maxItems)
                return false;
            else
                return true;
        });

        var dataLimit = data.length;
        $('a.more').click(function() {
            var moreFrom = parseInt($(this).data('from'), 10);
            var moreRange = moreFrom + maxItems;
            if (moreFrom >= dataLimit) {
                $(this).text('não há mais fotos');
                return false;
            }

            $.each(data, function(i, item) {
                if (i >= moreFrom && item.content) {
                    var $item;
                    if (item.media_type == 'image')
                        $item = $('<li id="item-' + i + '" class="item media image ' + item.date_posted + '"><a class="image-link" href="' + item.content + '" rel="shadowbox[baixocentro]" title="' + item.author + '"><img class="pic" width="240" src="/thumb/240x200/fit/' + item.content + '"></a><div class="meta"><p class="author">Autor: <strong>' + item.author + '</strong></p><p class="link"><a href="' + item.original_url + '" rel="external" target="_blank">Link original</a></p></div></li>');
                    else if (item.media_type == 'video')
                        $item = $('<li id="item-' + i + '" class="item media video ' + item.date_posted + '"><object width="490" height="275"><param name="movie" value="' + item.content + '"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><param name="wmode" value="transparent"></param><embed src="' + item.content + '" type="application/x-shockwave-flash" width="490" height="275" allowscriptaccess="always" allowfullscreen="true"></embed></object><div class="meta"><p class="author">Autor: <strong>' + item.author + '</strong></p><p class="link"><a href="' + item.original_url + '" rel="external" target="_blank">Link original</a></p></div></li>');
                    else if (item.media_type == 'text')
                        $item = $('<li id="item-' + i + '" class="item media text ' + item.date_posted + '"><p class="content">' + item.content + '</p><div class="meta"><p class="author">Autor: <strong>' + item.author + '</strong></p><p class="link"><a href="' + item.original_url + '" rel="external" target="_blank">Link original</a></p></div></li>');

                    $('#main.wall ul.content').append($item);
                    $item.hide();
                    $('#main.wall ul.content').imagesLoaded(function() {
                        Shadowbox.setup($(this).find('a.image-link'), {
                            gallery: 'baixocentro-' + reloadCount
                        });
                        $item.show();
                        $('#main.wall ul.content').masonry('reload');
                    });
                }

                if (i >= moreRange)
                    return false;
            });

            $(this).data('from', moreFrom+20);
            return false;
        });

        Shadowbox.init({skipSetup: true});
        Shadowbox.setup('a.image-link', {
            gallery: 'baixocentro-' + reloadCount
        });

        // masonry
        $('#main.wall ul.content').imagesLoaded(function() {
            $('section#main').fadeIn('fast');
            $('.loading').remove();
            $('#main.wall ul.content').masonry({
                // options
                itemSelector: 'li.item',
                columnWidth: 250,
                isFitWidth : true,
                isAnimated : true,
                animationOptions: {
                    duration: 750,
                    easing: 'linear',
                    queue: false
                }
            });
        });
    });

    var reloadCount = 0;
    $('a.reload').click(function() {
        $('li.item.media').remove();
            $.getJSON(jsonUrl, function(data) {

                data.sort(function(a,b) { return b.date_posted - a.date_posted; });
                var maxItems = 20;

                $.each(data, function(i, item) {
                    generateContent(i, item);
                        if (i >= maxItems)
                            return false;
                        else
                            return true;
                });

                $('#main.wall ul.content').imagesLoaded(function() {
                    $('#main.wall ul.content').masonry('reload');
                });

                $('a.more').data('from', 20);

                Shadowbox.setup('a.image-link', {
                    gallery: 'baixocentro-' + reloadCount
                });

                var dataLimit = data.length;
                reloadCount++;
            });
        return false;
    });
});

function generateContent(i, item) {
    if(item.content) {
    if(item.media_type == 'image')
        $('<li id="item-' + i + '" class="item media image ' + item.date_posted + '"><a class="image-link" href="' + item.content + '" rel="shadowbox[baixocentro]" title="' + item.author + '"><img class="pic" width="240" src="/thumb/240x200/fit/' + item.content + '" /></a><div class="meta"><p class="author">Autor: <strong>' + item.author + '</strong></p><p class="link"><a href="' + item.original_url + '" rel="external" target="_blank">Link original</a></p></div></li>').appendTo('#main.wall ul');
    else if(item.media_type == 'video')
    $('<li id="item-' + i + '" class="item media video ' + item.date_posted + '"><object width="490" height="275"><param name="movie" value="' + item.content + '"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><param name="wmode" value="transparent"></param><embed src="' + item.content + '" type="application/x-shockwave-flash" width="490" height="275" allowscriptaccess="always" allowfullscreen="true"></embed></object></iframe><div class="meta"><p class="author">Autor: <strong>' + item.author + '</strong></p><p class="link"><a href="' + item.original_url + '" rel="external" target="_blank">Link original</a></p></div></li>').appendTo('#main.wall ul');
    else if(item.media_type == 'text')
    $('<li id="item-' + i + '" class="item media text ' + item.date_posted + '"><p class="content">item.content</p><div class="meta"><p class="author">Autor: <strong>' + item.author + '</strong></p><p class="link"><a href="' + item.original_url + '" rel="external" target="_blank">Link original</a></p></div></li>').appendTo('#main.wall ul');
    }
}
