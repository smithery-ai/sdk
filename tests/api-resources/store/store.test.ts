// File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import Petstore from 'smithery';
import { Response } from 'node-fetch';

const client = new Petstore({
  apiKey: 'My API Key',
  baseURL: process.env['TEST_API_BASE_URL'] ?? 'http://127.0.0.1:4010',
});

describe('resource store', () => {
  test('createOrder', async () => {
    const responsePromise = client.store.createOrder();
    const rawResponse = await responsePromise.asResponse();
    expect(rawResponse).toBeInstanceOf(Response);
    const response = await responsePromise;
    expect(response).not.toBeInstanceOf(Response);
    const dataAndResponse = await responsePromise.withResponse();
    expect(dataAndResponse.data).toBe(response);
    expect(dataAndResponse.response).toBe(rawResponse);
  });

  test('createOrder: request options instead of params are passed correctly', async () => {
    // ensure the request options are being passed correctly by passing an invalid HTTP method in order to cause an error
    await expect(client.store.createOrder({ path: '/_stainless_unknown_path' })).rejects.toThrow(
      Petstore.NotFoundError,
    );
  });

  test('createOrder: request options and params are passed correctly', async () => {
    // ensure the request options are being passed correctly by passing an invalid HTTP method in order to cause an error
    await expect(
      client.store.createOrder(
        {
          id: 10,
          complete: true,
          petId: 198772,
          quantity: 7,
          shipDate: '2019-12-27T18:11:19.117Z',
          status: 'placed',
        },
        { path: '/_stainless_unknown_path' },
      ),
    ).rejects.toThrow(Petstore.NotFoundError);
  });

  test('inventory', async () => {
    const responsePromise = client.store.inventory();
    const rawResponse = await responsePromise.asResponse();
    expect(rawResponse).toBeInstanceOf(Response);
    const response = await responsePromise;
    expect(response).not.toBeInstanceOf(Response);
    const dataAndResponse = await responsePromise.withResponse();
    expect(dataAndResponse.data).toBe(response);
    expect(dataAndResponse.response).toBe(rawResponse);
  });

  test('inventory: request options instead of params are passed correctly', async () => {
    // ensure the request options are being passed correctly by passing an invalid HTTP method in order to cause an error
    await expect(client.store.inventory({ path: '/_stainless_unknown_path' })).rejects.toThrow(
      Petstore.NotFoundError,
    );
  });
});
