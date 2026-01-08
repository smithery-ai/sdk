// File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import type { Petstore } from '../client';

export abstract class APIResource {
  protected _client: Petstore;

  constructor(client: Petstore) {
    this._client = client;
  }
}
