// File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import { type Agent } from './_shims/index';
import * as qs from './internal/qs';
import * as Core from './core';
import * as Errors from './error';
import * as Uploads from './uploads';
import * as API from './resources/index';
import {
  APIResponse,
  Pet,
  PetCreateParams,
  PetFindByStatusParams,
  PetFindByStatusResponse,
  PetFindByTagsParams,
  PetFindByTagsResponse,
  PetUpdateByIDParams,
  PetUpdateParams,
  PetUploadImageParams,
  Pets,
} from './resources/pets';
import {
  User,
  UserCreateParams,
  UserCreateWithListParams,
  UserLoginParams,
  UserLoginResponse,
  UserResource,
  UserUpdateParams,
} from './resources/user';
import { Store, StoreCreateOrderParams, StoreInventoryResponse } from './resources/store/store';

export interface ClientOptions {
  /**
   * Defaults to process.env['PETSTORE_API_KEY'].
   */
  apiKey?: string | undefined;

  /**
   * Override the default base URL for the API, e.g., "https://api.example.com/v2/"
   *
   * Defaults to process.env['PETSTORE_BASE_URL'].
   */
  baseURL?: string | null | undefined;

  /**
   * The maximum amount of time (in milliseconds) that the client should wait for a response
   * from the server before timing out a single request.
   *
   * Note that request timeouts are retried by default, so in a worst-case scenario you may wait
   * much longer than this timeout before the promise succeeds or fails.
   */
  timeout?: number;

  /**
   * An HTTP agent used to manage HTTP(S) connections.
   *
   * If not provided, an agent will be constructed by default in the Node.js environment,
   * otherwise no agent is used.
   */
  httpAgent?: Agent;

  /**
   * Specify a custom `fetch` function implementation.
   *
   * If not provided, we use `node-fetch` on Node.js and otherwise expect that `fetch` is
   * defined globally.
   */
  fetch?: Core.Fetch | undefined;

  /**
   * The maximum number of times that the client will retry a request in case of a
   * temporary failure, like a network error or a 5XX error from the server.
   *
   * @default 2
   */
  maxRetries?: number;

  /**
   * Default headers to include with every request to the API.
   *
   * These can be removed in individual requests by explicitly setting the
   * header to `undefined` or `null` in request options.
   */
  defaultHeaders?: Core.Headers;

  /**
   * Default query parameters to include with every request to the API.
   *
   * These can be removed in individual requests by explicitly setting the
   * param to `undefined` in request options.
   */
  defaultQuery?: Core.DefaultQuery;
}

/**
 * API Client for interfacing with the Petstore API.
 */
export class Petstore extends Core.APIClient {
  apiKey: string;

  private _options: ClientOptions;

  /**
   * API Client for interfacing with the Petstore API.
   *
   * @param {string | undefined} [opts.apiKey=process.env['PETSTORE_API_KEY'] ?? undefined]
   * @param {string} [opts.baseURL=process.env['PETSTORE_BASE_URL'] ?? https://petstore3.swagger.io/api/v3] - Override the default base URL for the API.
   * @param {number} [opts.timeout=1 minute] - The maximum amount of time (in milliseconds) the client will wait for a response before timing out.
   * @param {number} [opts.httpAgent] - An HTTP agent used to manage HTTP(s) connections.
   * @param {Core.Fetch} [opts.fetch] - Specify a custom `fetch` function implementation.
   * @param {number} [opts.maxRetries=2] - The maximum number of times the client will retry a request.
   * @param {Core.Headers} opts.defaultHeaders - Default headers to include with every request to the API.
   * @param {Core.DefaultQuery} opts.defaultQuery - Default query parameters to include with every request to the API.
   */
  constructor({
    baseURL = Core.readEnv('PETSTORE_BASE_URL'),
    apiKey = Core.readEnv('PETSTORE_API_KEY'),
    ...opts
  }: ClientOptions = {}) {
    if (apiKey === undefined) {
      throw new Errors.PetstoreError(
        "The PETSTORE_API_KEY environment variable is missing or empty; either provide it, or instantiate the Petstore client with an apiKey option, like new Petstore({ apiKey: 'My API Key' }).",
      );
    }

    const options: ClientOptions = {
      apiKey,
      ...opts,
      baseURL: baseURL || `https://petstore3.swagger.io/api/v3`,
    };

    super({
      baseURL: options.baseURL!,
      timeout: options.timeout ?? 60000 /* 1 minute */,
      httpAgent: options.httpAgent,
      maxRetries: options.maxRetries,
      fetch: options.fetch,
    });

    this._options = options;

    this.apiKey = apiKey;
  }

  pets: API.Pets = new API.Pets(this);
  store: API.Store = new API.Store(this);
  user: API.UserResource = new API.UserResource(this);

  protected override defaultQuery(): Core.DefaultQuery | undefined {
    return this._options.defaultQuery;
  }

  protected override defaultHeaders(opts: Core.FinalRequestOptions): Core.Headers {
    return {
      ...super.defaultHeaders(opts),
      ...this._options.defaultHeaders,
    };
  }

  protected override authHeaders(opts: Core.FinalRequestOptions): Core.Headers {
    return { api_key: this.apiKey };
  }

  protected override stringifyQuery(query: Record<string, unknown>): string {
    return qs.stringify(query, { arrayFormat: 'comma' });
  }

  static Petstore = this;
  static DEFAULT_TIMEOUT = 60000; // 1 minute

  static PetstoreError = Errors.PetstoreError;
  static APIError = Errors.APIError;
  static APIConnectionError = Errors.APIConnectionError;
  static APIConnectionTimeoutError = Errors.APIConnectionTimeoutError;
  static APIUserAbortError = Errors.APIUserAbortError;
  static NotFoundError = Errors.NotFoundError;
  static ConflictError = Errors.ConflictError;
  static RateLimitError = Errors.RateLimitError;
  static BadRequestError = Errors.BadRequestError;
  static AuthenticationError = Errors.AuthenticationError;
  static InternalServerError = Errors.InternalServerError;
  static PermissionDeniedError = Errors.PermissionDeniedError;
  static UnprocessableEntityError = Errors.UnprocessableEntityError;

  static toFile = Uploads.toFile;
  static fileFromPath = Uploads.fileFromPath;
}

Petstore.Pets = Pets;
Petstore.Store = Store;
Petstore.UserResource = UserResource;
export declare namespace Petstore {
  export type RequestOptions = Core.RequestOptions;

  export {
    Pets as Pets,
    type APIResponse as APIResponse,
    type Pet as Pet,
    type PetFindByStatusResponse as PetFindByStatusResponse,
    type PetFindByTagsResponse as PetFindByTagsResponse,
    type PetCreateParams as PetCreateParams,
    type PetUpdateParams as PetUpdateParams,
    type PetFindByStatusParams as PetFindByStatusParams,
    type PetFindByTagsParams as PetFindByTagsParams,
    type PetUpdateByIDParams as PetUpdateByIDParams,
    type PetUploadImageParams as PetUploadImageParams,
  };

  export {
    Store as Store,
    type StoreInventoryResponse as StoreInventoryResponse,
    type StoreCreateOrderParams as StoreCreateOrderParams,
  };

  export {
    UserResource as UserResource,
    type User as User,
    type UserLoginResponse as UserLoginResponse,
    type UserCreateParams as UserCreateParams,
    type UserUpdateParams as UserUpdateParams,
    type UserCreateWithListParams as UserCreateWithListParams,
    type UserLoginParams as UserLoginParams,
  };

  export type Order = API.Order;
}

export { toFile, fileFromPath } from './uploads';
export {
  PetstoreError,
  APIError,
  APIConnectionError,
  APIConnectionTimeoutError,
  APIUserAbortError,
  NotFoundError,
  ConflictError,
  RateLimitError,
  BadRequestError,
  AuthenticationError,
  InternalServerError,
  PermissionDeniedError,
  UnprocessableEntityError,
} from './error';

export default Petstore;
