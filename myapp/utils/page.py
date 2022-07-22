from django.utils.safestring import mark_safe


class Page(object):
    def __init__(self, request, form, page_size=8, page_param='page', plus=5):
        self.page_size = page_size
        self.page = int(request.GET.get(page_param, 1))
        self.start = (self.page - 1) * page_size
        self.end = self.page * page_size
        self.page_form = form[self.start:self.end]

        total_count = form.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        if self.total_page_count <= 2 * self.plus + 1:
            self.start = 1
            self.end = self.total_page_count
        else:
            if (self.page + self.plus) > self.total_page_count:
                self.start = self.total_page_count - 2 * self.plus
                self.end = self.total_page_count
            elif (self.page - self.plus) < 1:
                self.start = 1
                self.end = self.plus * 2 + 1
            else:
                self.start = self.page - self.plus
                self.end = self.page + self.plus
        page_str_list = []
        if self.page > 1:
            prev = '<li><a href="?page={}">上一页</a></li>'.format(self.page - 1)
        else:
            prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
        page_str_list.append(prev)

        for i in range(self.start, self.end + 1):
            if i == self.page:
                ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
            else:
                ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
            page_str_list.append(ele)

        if self.page < self.total_page_count:
            prev = '<li><a href="?page={}">下一页</a></li>'.format(self.page + 1)
        else:
            prev = '<li><a href="?page={}">下一页</a></li>'.format(self.total_page_count)
        page_str_list.append(prev)
        page_string = mark_safe("".join(page_str_list))
        return page_string
