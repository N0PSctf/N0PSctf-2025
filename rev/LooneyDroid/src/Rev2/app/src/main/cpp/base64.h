//
// Created by Antonio on 27/02/2025.
//

#ifndef REV2_BASE64_H
#define REV2_BASE64_H

#include <vector>
#include <string>

std::string base64_encode(char const* buf, unsigned int bufLen);
char *base64_decode(std::string const&);

#endif //REV2_BASE64_H
