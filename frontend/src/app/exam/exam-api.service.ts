import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { API_URL } from '../env';
import { Exam } from './exam.model';

@Injectable()
export class ExamsApiService {

  constructor(private http: HttpClient) {
  }

  private static _handleError(err: HttpErrorResponse | any) {
    return throwError(err.message || 'Error: Unable to complete request.');
  }

  // GET list of public, future events
  getExams(): Observable<Exam[]> {
    return this.http
      .get(`${API_URL}/exams`)
      .pipe(ExamsApiService._handleError);
  }

  getTest(): Observable<string> {
    return this.http.get<Test>(`${API_URL}/test`).pipe(
      map((response:Test) => response.message)
    );
  }
}

interface Test {
  message: string;
}