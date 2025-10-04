import { TestBed } from '@angular/core/testing';

import { PublicationService } from './publication.services';

describe('Publication', () => {
  let service: PublicationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PublicationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
