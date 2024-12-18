// File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

export interface Order {
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
