# Github API Pagination Analysis

## Endpoint Tested
https://api.github.com/users/octocat/repos?page=1&per_page=5

## Objective
To analyze how GitHub paginates API responses.

## Headers
GitHub returns a "Link" header containing navigation URLs.
Ex: Link: <https://api.github.com/...page=2>; rel="next"

## Navigation Flow
Client reads Link header and follows rel="next" until rel="last".

## Conclusion
Pagination :
 reduces response size
 improves performance
 allows controlled data fetching
