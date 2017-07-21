from django.template import Library

# 加载过滤器的库
register = Library()


# 装饰自己写的filter
@register.filter
def multi(num1):
    # 乘以-1的作用就是点击之后，第一次升序排列，第二次降序排列
    return int(num1) * -1
