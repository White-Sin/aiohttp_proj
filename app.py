import aiohttp
from aiohttp import web
import json
from models import Ad, ads_db


# Создание нового объявления
async def create_ad(request):
    try:
        data = await request.json()
        
        # Проверка наличия всех обязательных полей
        if not data or not data.get('title') or not data.get('description') or not data.get('owner'):
            raise web.HTTPBadRequest(text="Missing required fields")
        
        ad = Ad(
            title=data['title'],
            description=data['description'],
            owner=data['owner']
        )
        
        # Сохраняем объявление в базу данных (в памяти)
        ads_db[ad.id] = ad
        
        return web.json_response(ad.to_dict(), status=201)
    
    except Exception as e:
        raise web.HTTPBadRequest(text=str(e))


# Получение всех объявлений
async def get_ads(request):
    return web.json_response([ad.to_dict() for ad in ads_db.values()])


# Получение конкретного объявления по ID
async def get_ad(request):
    ad_id = request.match_info['ad_id']
    ad = ads_db.get(ad_id)
    if not ad:
        raise web.HTTPNotFound(text="Ad not found")
    return web.json_response(ad.to_dict())


# Удаление объявления
async def delete_ad(request):
    ad_id = request.match_info['ad_id']
    ad = ads_db.pop(ad_id, None)
    if not ad:
        raise web.HTTPNotFound(text="Ad not found")
    return web.json_response({'message': 'Ad deleted successfully'}, status=200)


# Создание и настройка приложения aiohttp
async def init_app():
    app = web.Application()

    # Роуты
    app.router.add_post('/ads', create_ad)
    app.router.add_get('/ads', get_ads)
    app.router.add_get('/ads/{ad_id}', get_ad)
    app.router.add_delete('/ads/{ad_id}', delete_ad)

    return app


if __name__ == '__main__':
    app = init_app()
    web.run_app(app, host='0.0.0.0', port=8080)
