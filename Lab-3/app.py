from flask import Flask, render_template, redirect, url_for, request, Response
from src.bll.hotel_service import HotelService
from src.bll.export_system import ExporterFactory

app = Flask(__name__)
service = HotelService()

@app.route('/')
def index():
    hotels = service.get_all_hotels()
    return render_template('index.html', hotels=hotels)

@app.route('/add', methods=['GET', 'POST'])
def add_hotel():
    if request.method == 'POST':
        service.add_hotel(
            name=request.form['name'],
            star_rating=int(request.form['star_rating']),
            country=request.form['country'],
            city=request.form['city']
        )
        return redirect(url_for('index'))
        
    return render_template('add_hotel.html')

@app.route('/edit/<hotel_id>', methods=['GET', 'POST'])
def edit_hotel(hotel_id):
    if request.method == 'POST':
        service.update_hotel(
            hotel_id=hotel_id,
            name=request.form['name'],
            star_rating=int(request.form['star_rating']),
            country=request.form['country'],
            city=request.form['city']
        )
        return redirect(url_for('index'))
        
    hotel = service.get_hotel_by_id(hotel_id)
    return render_template('edit_hotel.html', hotel=hotel)

@app.route('/delete/<hotel_id>')
def delete_hotel(hotel_id):
    service.delete_hotel(hotel_id)
    return redirect(url_for('index'))

@app.route('/export/<format_type>')
def export_data(format_type):
    data = service.get_hotels_for_export()
    
    try:
        exporter = ExporterFactory.get_exporter(format_type)
        
        content = exporter.export(data)
        
        mimetype = 'application/json' if format_type == 'json' else 'application/xml'
        return Response(
            content, 
            mimetype=mimetype, 
            headers={"Content-disposition": f"attachment; filename=hotels_export.{format_type}"}
        )
    except ValueError as e:
        return str(e), 400
    
if __name__ == '__main__':
    app.run(debug=True)