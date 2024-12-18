// File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import Petstore from 'smithery';
import { Response } from 'node-fetch';

const client = new Petstore({
  apiKey: 'My API Key',
  baseURL: process.env['TEST_API_BASE_URL'] ?? 'http://127.0.0.1:4010',
});

describe('resource user', () => {
  test('create', async () => {
    const responsePromise = client.user.create();
    const rawResponse = await responsePromise.asResponse();
    expect(rawResponse).toBeInstanceOf(Response);
    const response = await responsePromise;
    expect(response).not.toBeInstanceOf(Response);
    const dataAndResponse = await responsePromise.withResponse();
    expect(dataAndResponse.data).toBe(response);
    expect(dataAndResponse.response).toBe(rawResponse);
  });

  test('create: request options instead of params are passed correctly', async () => {
    // ensure the request options are being passed correctly by passing an invalid HTTP method in order to cause an error
    await expect(client.user.create({ path: '/_stainless_unknown_path' })).rejects.toThrow(
      Petstore.NotFoundError,
    );
  });

  test('create: request options and params are passed correctly', async () => {
    // ensure the request options are being passed correctly by passing an invalid HTTP method in order to cause an error
    await expect(
      client.user.create(
        {
          id: 10,
          email: 'john@email.com',
          firstName: 'John',
          lastName: 'James',
          password: '12345',
          phone: '12345',
          username: 'theUser',
          userStatus: 1,
        },
        { path: '/_stainless_unknown_path' },
      ),
    ).rejects.toThrow(Petstore.NotFoundError);
  });

  test('retrieve', async () => {
    const responsePromise = client.user.retrieve('username');
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
    await expect(client.user.retrieve('username', { path: '/_stainless_unknown_path' })).rejects.toThrow(
      Petstore.NotFoundError,
    );
  });

  test('update', async () => {
    const responsePromise = client.user.update('username');
    const rawResponse = await responsePromise.asResponse();
    expect(rawResponse).toBeInstanceOf(Response);
    const response = await responsePromise;
    expect(response).not.toBeInstanceOf(Response);
    const dataAndResponse = await responsePromise.withResponse();
    expect(dataAndResponse.data).toBe(response);
    expect(dataAndResponse.response).toBe(rawResponse);
  });

  test('update: request options instead of params are passed correctly', async () => {
    // ensure the request options are being passed correctly by passing an invalid HTTP method in order to cause an error
    await expect(client.user.update('username', { path: '/_stainless_unknown_path' })).rejects.toThrow(
      Petstore.NotFoundError,
    );
  });

  test('update: request options and params are passed correctly', async () => {
    // ensure the request options are being passed correctly by passing an invalid HTTP method in order to cause an error
    await expect(
      client.user.update(
        'username',
        {
          id: 10,
          email: 'john@email.com',
          firstName: 'John',
          lastName: 'James',
          password: '12345',
          phone: '12345',
          username: 'theUser',
          userStatus: 1,
        },
        { path: '/_stainless_unknown_path' },
      ),
    ).rejects.toThrow(Petstore.NotFoundError);
  });

  test('delete', async () => {
    const responsePromise = client.user.delete('username');
    const rawResponse = await responsePromise.asResponse();
    expect(rawResponse).toBeInstanceOf(Response);
    const response = await responsePromise;
    expect(response).not.toBeInstanceOf(Response);
    const dataAndResponse = await responsePromise.withResponse();
    expect(dataAndResponse.data).toBe(response);
    expect(dataAndResponse.response).toBe(rawResponse);
  });

  test('delete: request options instead of params are passed correctly', async () => {
    // ensure the request options are being passed correctly by passing an invalid HTTP method in order to cause an error
    await expect(client.user.delete('username', { path: '/_stainless_unknown_path' })).rejects.toThrow(
      Petstore.NotFoundError,
    );
  });

  test('createWithList: only required params', async () => {
    const responsePromise = client.user.createWithList([{}]);
    const rawResponse = await responsePromise.asResponse();
    expect(rawResponse).toBeInstanceOf(Response);
    const response = await responsePromise;
    expect(response).not.toBeInstanceOf(Response);
    const dataAndResponse = await responsePromise.withResponse();
    expect(dataAndResponse.data).toBe(response);
    expect(dataAndResponse.response).toBe(rawResponse);
  });

  test('createWithList: required and optional params', async () => {
    const response = await client.user.createWithList([
      {
        id: 10,
        email: 'john@email.com',
        firstName: 'John',
        lastName: 'James',
        password: '12345',
        phone: '12345',
        username: 'theUser',
        userStatus: 1,
      },
    ]);
  });

  test('login', async () => {
    const responsePromise = client.user.login();
    const rawResponse = await responsePromise.asResponse();
    expect(rawResponse).toBeInstanceOf(Response);
    const response = await responsePromise;
    expect(response).not.toBeInstanceOf(Response);
    const dataAndResponse = await responsePromise.withResponse();
    expect(dataAndResponse.data).toBe(response);
    expect(dataAndResponse.response).toBe(rawResponse);
  });

  test('login: request options instead of params are passed correctly', async () => {
    // ensure the request options are being passed correctly by passing an invalid HTTP method in order to cause an error
    await expect(client.user.login({ path: '/_stainless_unknown_path' })).rejects.toThrow(
      Petstore.NotFoundError,
    );
  });

  test('login: request options and params are passed correctly', async () => {
    // ensure the request options are being passed correctly by passing an invalid HTTP method in order to cause an error
    await expect(
      client.user.login({ password: 'password', username: 'username' }, { path: '/_stainless_unknown_path' }),
    ).rejects.toThrow(Petstore.NotFoundError);
  });

  test('logout', async () => {
    const responsePromise = client.user.logout();
    const rawResponse = await responsePromise.asResponse();
    expect(rawResponse).toBeInstanceOf(Response);
    const response = await responsePromise;
    expect(response).not.toBeInstanceOf(Response);
    const dataAndResponse = await responsePromise.withResponse();
    expect(dataAndResponse.data).toBe(response);
    expect(dataAndResponse.response).toBe(rawResponse);
  });

  test('logout: request options instead of params are passed correctly', async () => {
    // ensure the request options are being passed correctly by passing an invalid HTTP method in order to cause an error
    await expect(client.user.logout({ path: '/_stainless_unknown_path' })).rejects.toThrow(
      Petstore.NotFoundError,
    );
  });
});
