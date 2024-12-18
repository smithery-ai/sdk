// File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import Petstore, { toFile } from 'smithery';
import { Response } from 'node-fetch';

const client = new Petstore({
  apiKey: 'My API Key',
  baseURL: process.env['TEST_API_BASE_URL'] ?? 'http://127.0.0.1:4010',
});

describe('resource pets', () => {
  test('create: only required params', async () => {
    const responsePromise = client.pets.create({ name: 'doggie', photoUrls: ['string'] });
    const rawResponse = await responsePromise.asResponse();
    expect(rawResponse).toBeInstanceOf(Response);
    const response = await responsePromise;
    expect(response).not.toBeInstanceOf(Response);
    const dataAndResponse = await responsePromise.withResponse();
    expect(dataAndResponse.data).toBe(response);
    expect(dataAndResponse.response).toBe(rawResponse);
  });

  test('create: required and optional params', async () => {
    const response = await client.pets.create({
      name: 'doggie',
      photoUrls: ['string'],
      id: 10,
      category: { id: 1, name: 'Dogs' },
      status: 'available',
      tags: [{ id: 0, name: 'name' }],
    });
  });

  test('retrieve', async () => {
    const responsePromise = client.pets.retrieve(0);
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
    await expect(client.pets.retrieve(0, { path: '/_stainless_unknown_path' })).rejects.toThrow(
      Petstore.NotFoundError,
    );
  });

  test('update: only required params', async () => {
    const responsePromise = client.pets.update({ name: 'doggie', photoUrls: ['string'] });
    const rawResponse = await responsePromise.asResponse();
    expect(rawResponse).toBeInstanceOf(Response);
    const response = await responsePromise;
    expect(response).not.toBeInstanceOf(Response);
    const dataAndResponse = await responsePromise.withResponse();
    expect(dataAndResponse.data).toBe(response);
    expect(dataAndResponse.response).toBe(rawResponse);
  });

  test('update: required and optional params', async () => {
    const response = await client.pets.update({
      name: 'doggie',
      photoUrls: ['string'],
      id: 10,
      category: { id: 1, name: 'Dogs' },
      status: 'available',
      tags: [{ id: 0, name: 'name' }],
    });
  });

  test('delete', async () => {
    const responsePromise = client.pets.delete(0);
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
    await expect(client.pets.delete(0, { path: '/_stainless_unknown_path' })).rejects.toThrow(
      Petstore.NotFoundError,
    );
  });

  test('findByStatus', async () => {
    const responsePromise = client.pets.findByStatus();
    const rawResponse = await responsePromise.asResponse();
    expect(rawResponse).toBeInstanceOf(Response);
    const response = await responsePromise;
    expect(response).not.toBeInstanceOf(Response);
    const dataAndResponse = await responsePromise.withResponse();
    expect(dataAndResponse.data).toBe(response);
    expect(dataAndResponse.response).toBe(rawResponse);
  });

  test('findByStatus: request options instead of params are passed correctly', async () => {
    // ensure the request options are being passed correctly by passing an invalid HTTP method in order to cause an error
    await expect(client.pets.findByStatus({ path: '/_stainless_unknown_path' })).rejects.toThrow(
      Petstore.NotFoundError,
    );
  });

  test('findByStatus: request options and params are passed correctly', async () => {
    // ensure the request options are being passed correctly by passing an invalid HTTP method in order to cause an error
    await expect(
      client.pets.findByStatus({ status: 'available' }, { path: '/_stainless_unknown_path' }),
    ).rejects.toThrow(Petstore.NotFoundError);
  });

  test('findByTags', async () => {
    const responsePromise = client.pets.findByTags();
    const rawResponse = await responsePromise.asResponse();
    expect(rawResponse).toBeInstanceOf(Response);
    const response = await responsePromise;
    expect(response).not.toBeInstanceOf(Response);
    const dataAndResponse = await responsePromise.withResponse();
    expect(dataAndResponse.data).toBe(response);
    expect(dataAndResponse.response).toBe(rawResponse);
  });

  test('findByTags: request options instead of params are passed correctly', async () => {
    // ensure the request options are being passed correctly by passing an invalid HTTP method in order to cause an error
    await expect(client.pets.findByTags({ path: '/_stainless_unknown_path' })).rejects.toThrow(
      Petstore.NotFoundError,
    );
  });

  test('findByTags: request options and params are passed correctly', async () => {
    // ensure the request options are being passed correctly by passing an invalid HTTP method in order to cause an error
    await expect(
      client.pets.findByTags({ tags: ['string'] }, { path: '/_stainless_unknown_path' }),
    ).rejects.toThrow(Petstore.NotFoundError);
  });

  test('updateById', async () => {
    const responsePromise = client.pets.updateById(0);
    const rawResponse = await responsePromise.asResponse();
    expect(rawResponse).toBeInstanceOf(Response);
    const response = await responsePromise;
    expect(response).not.toBeInstanceOf(Response);
    const dataAndResponse = await responsePromise.withResponse();
    expect(dataAndResponse.data).toBe(response);
    expect(dataAndResponse.response).toBe(rawResponse);
  });

  test('updateById: request options instead of params are passed correctly', async () => {
    // ensure the request options are being passed correctly by passing an invalid HTTP method in order to cause an error
    await expect(client.pets.updateById(0, { path: '/_stainless_unknown_path' })).rejects.toThrow(
      Petstore.NotFoundError,
    );
  });

  test('updateById: request options and params are passed correctly', async () => {
    // ensure the request options are being passed correctly by passing an invalid HTTP method in order to cause an error
    await expect(
      client.pets.updateById(0, { name: 'name', status: 'status' }, { path: '/_stainless_unknown_path' }),
    ).rejects.toThrow(Petstore.NotFoundError);
  });

  test('uploadImage: only required params', async () => {
    const responsePromise = client.pets.uploadImage(0, {
      image: await toFile(Buffer.from('# my file contents'), 'README.md'),
    });
    const rawResponse = await responsePromise.asResponse();
    expect(rawResponse).toBeInstanceOf(Response);
    const response = await responsePromise;
    expect(response).not.toBeInstanceOf(Response);
    const dataAndResponse = await responsePromise.withResponse();
    expect(dataAndResponse.data).toBe(response);
    expect(dataAndResponse.response).toBe(rawResponse);
  });

  test('uploadImage: required and optional params', async () => {
    const response = await client.pets.uploadImage(0, {
      image: await toFile(Buffer.from('# my file contents'), 'README.md'),
      additionalMetadata: 'additionalMetadata',
    });
  });
});
