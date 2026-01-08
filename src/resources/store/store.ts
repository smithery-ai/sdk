// File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import { APIResource } from '../../core/resource';
import * as Shared from '../shared';
import * as OrderAPI from './order';
import { Order } from './order';
import { APIPromise } from '../../core/api-promise';
import { RequestOptions } from '../../internal/request-options';

export class Store extends APIResource {
  order: OrderAPI.Order = new OrderAPI.Order(this._client);

  /**
   * Place a new order in the store
   *
   * @example
   * ```ts
   * const order = await client.store.createOrder();
   * ```
   */
  createOrder(
    body: StoreCreateOrderParams | null | undefined = {},
    options?: RequestOptions,
  ): APIPromise<Shared.Order> {
    return this._client.post('/store/order', { body, ...options });
  }

  /**
   * Returns a map of status codes to quantities
   *
   * @example
   * ```ts
   * const response = await client.store.inventory();
   * ```
   */
  inventory(options?: RequestOptions): APIPromise<StoreInventoryResponse> {
    return this._client.get('/store/inventory', options);
  }
}

export type StoreInventoryResponse = { [key: string]: number };

export interface StoreCreateOrderParams {
  id?: number;

  complete?: boolean;

  petId?: number;

  quantity?: number;

  shipDate?: string;

  /**
   * Order Status
   */
  status?: 'placed' | 'approved' | 'delivered';
}

Store.Order = Order;

export declare namespace Store {
  export {
    type StoreInventoryResponse as StoreInventoryResponse,
    type StoreCreateOrderParams as StoreCreateOrderParams,
  };

  export { Order as Order };
}
