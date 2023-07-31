import { Component, OnDestroy, OnInit } from '@angular/core';
import { DocumentApiService, SearchResult, Occurrence } from './documentSearch/document-api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.less']
})
export class AppComponent implements OnInit {
  title = 'frontend';

  test: string = "";

  private readonly _filename = "king-i-150";
  private _searchInput: string = "";
  private _isSearch: boolean = false;
  private _isButtonDisabled: boolean = false;
  documents: string = "";
  searchResult: SearchResult = {};

  constructor(
    private documentsApi: DocumentApiService
  ) {
  }

  ngOnInit() {
    this.documentsApi.initDoc(this._filename).subscribe((content: string) => {
      this.documents = content ?? "";
    });
  }

  get isValidDocument(): boolean {
    return this.documents !== undefined && this.documents !== '';
  }

  get isSearch(): boolean {
    return this._isSearch;
  }

  get isSearchResultFound(): boolean {
    return this.searchResult.occurences !== undefined && this.searchResult.occurences.length !== 0;
  }

  get isButtonDisabled(): boolean {
    return this._isButtonDisabled;
  }

  set searchInput(value: string) {
    this._searchInput = value ?? '';
  }

  searchText() {
    this._isButtonDisabled = true;
    this.test = this._searchInput;
    this.documentsApi.searchText(this._filename, this.test).subscribe((response: SearchResult) => {
      this.searchResult = response;
      this._isSearch = true;
      this._isButtonDisabled = false;
    });
    return;
  }
}
