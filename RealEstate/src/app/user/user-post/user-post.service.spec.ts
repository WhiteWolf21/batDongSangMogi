import { TestBed } from '@angular/core/testing';

import { UserPostService } from './user-post.service';

describe('UserPostService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: UserPostService = TestBed.get(UserPostService);
    expect(service).toBeTruthy();
  });
});
