from haystack.generic_views import SearchView


class MySearchView(SearchView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cart_show'] = '1'
        context['title'] = '商品搜索结果'
        # 存放页码
        page_list = []
        # 拿到页面中的page对象
        page_obj = context['page_obj']
        # 页面总数小于5页，显示1,2,3,4,5
        if page_obj.paginator.num_pages < 5:
            page_list = range(1, page_obj.paginator.num_pages + 1)
        # 当前页面小于等于2页，显示1,2,3,4,5
        elif page_obj.number <= 2:
            page_list = range(1, 5 + 1)
        # 倒数第2页和倒数第1页，显示6,7,8,9,10
        elif page_obj.number >= page_obj.paginator.num_pages - 1:
            page_list = range(page_obj.paginator.num_pages - 5 + 1, page_obj.paginator.num_pages + 1)
        else:
            # 其他正常显示页面，显示3,4,5,6,7
            page_list = range(page_obj.number - 2, page_obj.number + 3)
        context['page_list'] = page_list
        return context
