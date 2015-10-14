from calendar import Calendar
from datetime import datetime
from lxml import etree

def get_url(i):
    return '/go/to/%s' % i

class ComicCalendar(Calendar):

    def getMonthCalendar(self, current_date, date_list=[], url_method=get_url):
        
        # Get current month date
        date_obj = self.get_date(current_date)
        (year, month, day) = self.get_ymd(date_obj)

        # Get weekly data
        data = self.monthdatescalendar(year, month)

        # Create parent calendar element        
        calendar = etree.Element("div", klass="calendar")
        
        # Add month title
        month_header = etree.Element("div", klass="month")
        month_header.text = date_obj.strftime('%B %Y')
        calendar.append(month_header)

        # Add weekday blocks
        week_header = etree.Element("div", klass="week-header week")
        
        for i in data[0]:
            day_header = etree.Element("div", klass="day-header day")
            day_header.text = i.strftime('%a')
            
            week_header.append(day_header)
        
        calendar.append(week_header)

        for w in data:
            week_data = etree.Element("div", klass="week")
            
            for d in w:
                day_data = etree.Element("div", klass="day")
                
                if d.month == month and d.year == year:
                    fmt_date = d.strftime('%Y%m%d')
                    fmt_day = d.strftime('%-d')
                    if fmt_date in date_list:
                        klass = ""
                    
                        if d.day == day:
                            klass = "current"
                    
                        a = etree.Element("a", klass=klass, href=url_method(fmt_date))
                        a.text = fmt_day
                        
                        day_data.append(a)
                    else:
                        day_data.text = fmt_day
                else:
                    day_data.text = 'EMPTY_CELL'
                    
                week_data.append(day_data)
            
            calendar.append(week_data)
        
        visual_clear = etree.Element("div", klass="visualClear")
        visual_clear.text = 'EMPTY_COMMENT'
        
        calendar.append(visual_clear)
        
        text = etree.tostring(calendar)
        
        return text.replace('klass', 'class').replace('EMPTY_CELL', '&nbsp;').replace('EMPTY_COMMENT', '<!-- -->')

    def get_date(self, i):
        try:
            return datetime.strptime(i, '%Y%m%d')
        except:
            return None

    def get_ymd(self, i):
        return (i.year, i.month, i.day)
