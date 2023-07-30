import { Component, OnDestroy, OnInit } from '@angular/core';
import { Exam } from './exam/exam.model';
import { Observable, Subscription } from 'rxjs';
import { ExamsApiService } from './exam/exam-api.service';
import { DocumentApiService } from './exam/document-api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.less']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'frontend';
  //examsListSubs!: Subscription;
  //examsList!: Exam[];

  testRequest: string = "";
  test: string = "";

  private readonly _filename = "king-i-150";
  private _searchInput: string = "";
  documents: string = "";

  constructor(
    private examsApi: ExamsApiService,
    private documentsApi: DocumentApiService
  ) {
  }

  ngOnInit() {
    // this.examsListSubs = this.examsApi
    //   .getExams()
    //   .subscribe(res => {
    //       this.examsList = res;
    //     },
    //     console.error
    //   );
    this.documentsApi.initDocDict().subscribe((error: any)=>{console.error("Error initializing dictionaries", error);});
    this.documentsApi.initDoc(this._filename).subscribe((content: string) => {
      this.documents = content ?? "";
    });
  }

  get isValidDocument(): boolean {
    return this.documents !== undefined && this.documents !== '';
  }

  set searchInput(value: string) {
    this._searchInput = value ?? '';
  }

  searchText() {
    this.test = this._searchInput;
    return;
  }

  TriggerRequest() {
    this.examsApi.getTest().subscribe((message:string) => {
      this.testRequest = message;
    });
    console.log(this.testRequest);
  }

  ngOnDestroy() {
    //this.examsListSubs.unsubscribe();
  }
}
