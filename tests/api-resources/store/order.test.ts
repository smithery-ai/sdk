// File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import Petstore from 'smithery';
import { Response } from 'node-fetch';

const client = new Petstore({
  apiKey: 'My API Key',
  baseURL: process.env['TEST_API_BASE_URL'] ?? 'http://127.0.0.1:4010',
});

describe('resource order', () => {
  test('retrieve', async () => {
    const responsePromise = client.store.order.retrieve(0);
    const rawResponse = await responsePromise.asResponse();
    expect(rawResponse).toBeInstanceOf(Response);
    const response = await responsePromise;
    expect(response).not.toBeInstanceOf(Response);
    const dataAndResponse = await responsePromise.withResponse();
    expect(dataAndResponse.data).toBe(response);
    expect(dataAndResponse.response).toBe(rawResponse);
  });

  test('retrieve: request options instead of params are passed correctly', async () => {
    // ensure the request options are being passed correctly by passing an invalid HTTP method in order to cause an error
    await expect(client.store.order.retrieve(0, { path: '/_stainless_unknown_path' })).rejects.toThrow(
      Petstore.NotFoundError,
    );
  });

  test('deleteOrder', async () => {
    const responsePromise = client.store.order.deleteOrder(0);
    const rawResponse = await responsePromise.asResponse();
    expect(rawResponse).toBeInstanceOf(Response);
    const response = await responsePromise;
    expect(response).not.toBeInstanceOf(Response);
    const dataAndResponse = await responsePromise.withResponse();
    expect(dataAndResponse.data).toBe(response);
    expect(dataAndResponse.response).toBe(rawResponse);
  });

  test('deleteOrder: request options instead of params are passed correctly', async () => {
    // ensure the request options are being passed correctly by passing an invalid HTTP method in order to cause an error
    await expect(client.store.order.deleteOrder(0, { path: '/_stainless_unknown_path' })).rejects.toThrow(
      Petstore.NotFoundError,
    );
  });
});
