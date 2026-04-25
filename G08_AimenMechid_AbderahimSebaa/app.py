"""
تطبيق Flask لإدارة الرحلات - Part 2
يستخدم DOM للبحث و ElementTree للإحصائيات والتصفية
"""

from flask import Flask, render_template, request, jsonify
from xml.dom import minidom
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)

# تحديد مسار ملف XML
XML_FILE = os.path.join(os.path.dirname(__file__), 'transport.xml')


# ==================== دوال مساعدة ====================

def get_stations():
    """جلب قائمة جميع المحطات من XML باستخدام ElementTree"""
    try:
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
        
        stations = {}
        for station in root.find('stations').findall('station'):
            stations[station.get('id')] = station.get('name')
        
        return stations
    except Exception as e:
        print(f"خطأ في قراءة المحطات: {e}")
        return {}


def get_all_trips():
    """
    قراءة جميع الرحلات من ملف XML
    تستخدم ElementTree للمعالجة
    """
    try:
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
        stations = get_stations()
        
        trips = []
        
        for line in root.find('lines').findall('line'):
            line_code = line.get('code')
            departure_id = line.get('departure')
            arrival_id = line.get('arrival')
            
            departure_name = stations.get(departure_id, departure_id)
            arrival_name = stations.get(arrival_id, arrival_id)
            
            for trip in line.find('trips').findall('trip'):
                trip_code = trip.get('code')
                train_type = trip.get('type')
                schedule = trip.find('schedule')
                departure_time = schedule.get('departure')
                arrival_time = schedule.get('arrival')
                days_elem = trip.find('days')
                days = days_elem.text if days_elem is not None else "كل الأيام"
                
                # جمع جميع الدرجات (Economy, VIP)
                classes = []
                for class_elem in trip.findall('class'):
                    classes.append({
                        'type': class_elem.get('type'),
                        'price': int(class_elem.get('price'))
                    })
                
                # حساب أقل سعر في الرحلة
                min_price = min(c['price'] for c in classes) if classes else 0
                
                trips.append({
                    'code': trip_code,
                    'line_code': line_code,
                    'departure': departure_name,
                    'departure_id': departure_id,
                    'arrival': arrival_name,
                    'arrival_id': arrival_id,
                    'departure_time': departure_time,
                    'arrival_time': arrival_time,
                    'schedule': f"{departure_time} - {arrival_time}",
                    'train_type': train_type,
                    'days': days,
                    'classes': classes,
                    'min_price': min_price
                })
        
        return trips
    except Exception as e:
        print(f"خطأ في قراءة الرحلات: {e}")
        return []


# ==================== البحث باستخدام DOM (مطلوب) ====================

def search_trip_by_code_dom(trip_code):
    """
    البحث عن رحلة برمزها باستخدام DOM
    هذا مطلوب في التعليمات
    """
    try:
        dom = minidom.parse(XML_FILE)
        
        # جلب المحطات
        stations_dom = dom.getElementsByTagName('stations')[0]
        stations = {}
        for station in stations_dom.getElementsByTagName('station'):
            stations[station.getAttribute('id')] = station.getAttribute('name')
        
        # البحث في الخطوط
        lines = dom.getElementsByTagName('lines')[0]
        for line in lines.getElementsByTagName('line'):
            departure_id = line.getAttribute('departure')
            arrival_id = line.getAttribute('arrival')
            
            for trip in line.getElementsByTagName('trip'):
                if trip.getAttribute('code') == trip_code:
                    train_type = trip.getAttribute('type')
                    schedule = trip.getElementsByTagName('schedule')[0]
                    departure_time = schedule.getAttribute('departure')
                    arrival_time = schedule.getAttribute('arrival')
                    
                    # جلب الدرجات
                    classes = []
                    for class_elem in trip.getElementsByTagName('class'):
                        classes.append({
                            'type': class_elem.getAttribute('type'),
                            'price': int(class_elem.getAttribute('price'))
                        })
                    
                    days_elem = trip.getElementsByTagName('days')
                    days = days_elem[0].firstChild.data if days_elem and days_elem[0].firstChild else "كل الأيام"
                    
                    return {
                        'code': trip_code,
                        'departure': stations.get(departure_id, departure_id),
                        'arrival': stations.get(arrival_id, arrival_id),
                        'departure_time': departure_time,
                        'arrival_time': arrival_time,
                        'schedule': f"{departure_time} - {arrival_time}",
                        'train_type': train_type,
                        'days': days,
                        'classes': classes
                    }
        
        return None
    except Exception as e:
        print(f"خطأ في البحث DOM: {e}")
        return None


# ==================== الإحصائيات باستخدام ElementTree (مطلوب) ====================

def get_statistics():
    """
    حساب الإحصائيات المطلوبة باستخدام ElementTree:
    - أرخص وأغلى رحلة لكل خط
    - عدد الرحلات لكل نوع قطار
    """
    try:
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
        stations = get_stations()
        
        # إحصائيات أنواع القطارات
        train_type_count = {}
        
        # إحصائيات لكل خط
        lines_stats = {}
        
        # قائمة بكل الرحلات لأرخص وأغلى رحلة عامة
        all_trips = []
        
        for line in root.find('lines').findall('line'):
            line_code = line.get('code')
            departure_id = line.get('departure')
            arrival_id = line.get('arrival')
            departure_name = stations.get(departure_id, departure_id)
            arrival_name = stations.get(arrival_id, arrival_id)
            line_key = f"{departure_name} → {arrival_name}"
            
            # تخزين مؤقت لأسعار هذا الخط
            line_trips_info = []
            
            for trip in line.find('trips').findall('trip'):
                train_type = trip.get('type')
                
                # تحديث عدد الرحلات حسب نوع القطار
                train_type_count[train_type] = train_type_count.get(train_type, 0) + 1
                
                # جمع أسعار هذه الرحلة
                prices = [int(c.get('price')) for c in trip.findall('class')]
                if prices:
                    min_price = min(prices)
                    max_price = max(prices)
                    line_trips_info.append({
                        'code': trip.get('code'),
                        'min_price': min_price,
                        'max_price': max_price
                    })
                    all_trips.append({
                        'code': trip.get('code'),
                        'train_type': train_type,
                        'price': min_price,
                        'line': line_key
                    })
            
            # تحديد أرخص وأغلى رحلة في هذا الخط
            if line_trips_info:
                min_trip = min(line_trips_info, key=lambda x: x['min_price'])
                max_trip = max(line_trips_info, key=lambda x: x['max_price'])
                lines_stats[line_key] = {
                    'line_code': line_code,
                    'departure': departure_name,
                    'arrival': arrival_name,
                    'min_price': min_trip['min_price'],
                    'max_price': max_trip['max_price'],
                    'min_trip_code': min_trip['code'],
                    'max_trip_code': max_trip['code']
                }
        
        # أرخص وأغلى رحلة بشكل عام
        cheapest = min(all_trips, key=lambda x: x['price']) if all_trips else None
        most_expensive = max(all_trips, key=lambda x: x['price']) if all_trips else None
        
        return {
            'train_type_count': train_type_count,
            'lines_stats': list(lines_stats.values()),
            'total_trips': len(all_trips),
            'cheapest_trip': cheapest,
            'most_expensive_trip': most_expensive
        }
    except Exception as e:
        print(f"خطأ في حساب الإحصائيات: {e}")
        return {
            'train_type_count': {},
            'lines_stats': [],
            'total_trips': 0,
            'cheapest_trip': None,
            'most_expensive_trip': None
        }


# ==================== دوال التصفية ====================

def filter_trips(departure=None, arrival=None, train_type=None, max_price=None):
    """
    تصفية الرحلات حسب المعايير المختلفة
    """
    all_trips = get_all_trips()
    filtered = all_trips
    
    # تصفية حسب مدينة المغادرة
    if departure and departure != '':
        filtered = [t for t in filtered if t['departure'].lower() == departure.lower()]
    
    # تصفية حسب مدينة الوصول
    if arrival and arrival != '':
        filtered = [t for t in filtered if t['arrival'].lower() == arrival.lower()]
    
    # تصفية حسب نوع القطار
    if train_type and train_type != '':
        filtered = [t for t in filtered if t['train_type'].lower() == train_type.lower()]
    
    # تصفية حسب السعر الأقصى
    if max_price and max_price != '':
        max_price = int(max_price)
        filtered = [t for t in filtered if t['min_price'] <= max_price]
    
    return filtered


# ==================== مسارات Flask (API) ====================

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    return render_template('index.html')


@app.route('/api/trips')
def get_trips():
    """API لجلب الرحلات مع التصفية"""
    departure = request.args.get('departure', '')
    arrival = request.args.get('arrival', '')
    train_type = request.args.get('train_type', '')
    max_price = request.args.get('max_price', '')
    
    trips = filter_trips(departure, arrival, train_type, max_price)
    return jsonify(trips)


@app.route('/api/trip/<code>')
def get_trip_by_code(code):
    """
    API للبحث عن رحلة برمزها
    يستخدم DOM كما هو مطلوب في التعليمات
    """
    trip = search_trip_by_code_dom(code)
    if trip:
        return jsonify(trip)
    return jsonify({'error': 'لم يتم العثور على الرحلة'}), 404


@app.route('/api/statistics')
def get_statistics_api():
    """API لجلب الإحصائيات (باستخدام ElementTree)"""
    stats = get_statistics()
    return jsonify(stats)


@app.route('/api/cities')
def get_cities():
    """API لجلب قائمة المدن وأنواع القطارات"""
    trips = get_all_trips()
    
    departures = list(set(t['departure'] for t in trips))
    arrivals = list(set(t['arrival'] for t in trips))
    train_types = list(set(t['train_type'] for t in trips))
    
    return jsonify({
        'departures': sorted(departures),
        'arrivals': sorted(arrivals),
        'train_types': sorted(train_types)
    })


if __name__ == '__main__':
    app.run(debug=True)