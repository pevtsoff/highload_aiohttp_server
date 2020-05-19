import string, random, asyncio
from aiohttp.web import (Response, StreamResponse, RouteTableDef,
                         Application, run_app, HTTPTemporaryRedirect)

routes = RouteTableDef()
chunk_size = 100 # number of chars sent to client


@routes.get('/test_endpoint', name='test_endpoint')
async def final_endpoint(request):
    response = StreamResponse(
        status=200,
        reason='OK',
        headers={'Content-Type': 'text/plain'}
    )
    await response.prepare(request)
    await _write_resp(response)
    response.force_close()

    return response


async def _write_resp(response):
    async for line in _gen_rnd_data():
        await response.write(line.encode('utf-8'))

    await response.write_eof()


async def _gen_rnd_data(chunk_size=chunk_size):
    letters = string.ascii_lowercase
    
    while True: 
        yield ''.join(random.choice(letters) for i in range(chunk_size))
        # this timeout is to make http server more responsive and 
        # able to handle thousands concurrent connections
        await asyncio.sleep(0.001)
        

if __name__ == '__main__':
    app = Application(debug=True)
    app.add_routes(routes)
    run_app(app, port=9005)





